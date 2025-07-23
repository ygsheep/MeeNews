from rest_framework import viewsets, permissions
from .models import Comment, Like, Share, Report, PlayHistory, Favorite, UserBehaviorStats, ContentInteractionStats, UserProfile, Recommendation, TrendingTopic
from .serializers import CommentSerializer, LikeSerializer, ShareSerializer, ReportSerializer, PlayHistorySerializer, FavoriteSerializer, UserBehaviorStatsSerializer, ContentInteractionStatsSerializer, UserProfileSerializer, RecommendationSerializer, TrendingTopicSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from django.db.models import Sum, Count, Avg, Max
from rest_framework import status
import random

class CommentViewSet(viewsets.ModelViewSet):
    """评论API，支持增删改查、嵌套、权限"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LikeViewSet(viewsets.ModelViewSet):
    """点赞/点踩API，支持幂等、权限"""
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ShareViewSet(viewsets.ModelViewSet):
    """分享API，支持权限"""
    queryset = Share.objects.all()
    serializer_class = ShareSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@extend_schema(tags=["举报"], summary="举报管理", description="举报内容、评论等，支持增删查。")
class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    @extend_schema(summary="批量删除举报", request=None, responses={204: OpenApiResponse(description="删除成功")})
    @action(detail=False, methods=['delete'], url_path='batch-delete')
    def batch_delete(self, request):
        ids = request.data.get('ids', [])
        Report.objects.filter(id__in=ids, user=request.user).delete()
        return Response({'success': True, 'message': '批量删除成功'})

@extend_schema(tags=["播放历史"], summary="播放历史管理", description="记录和查询用户播放历史。")
class PlayHistoryViewSet(viewsets.ModelViewSet):
    queryset = PlayHistory.objects.all()
    serializer_class = PlayHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        # 只允许用户访问自己的播放历史
        return PlayHistory.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    @extend_schema(summary="批量删除播放历史", request=None, responses={204: OpenApiResponse(description="删除成功")})
    @action(detail=False, methods=['delete'], url_path='batch-delete')
    def batch_delete(self, request):
        ids = request.data.get('ids', [])
        PlayHistory.objects.filter(id__in=ids, user=request.user).delete()
        return Response({'success': True, 'message': '批量删除成功'})
    @extend_schema(summary="统计总播放时长", responses={200: OpenApiResponse(description="总播放时长(秒)")})
    @action(detail=False, methods=['get'], url_path='total-duration')
    def total_duration(self, request):
        total = self.get_queryset().aggregate(total=Sum('play_duration'))['total'] or 0
        return Response({'total_play_duration': total})

@extend_schema(tags=["收藏"], summary="收藏管理", description="收藏内容，支持批量操作。")
class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        # 只允许用户访问自己的收藏
        return Favorite.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    @extend_schema(summary="批量收藏", request=None, responses={200: OpenApiResponse(description="批量收藏成功")})
    @action(detail=False, methods=['post'], url_path='batch-create')
    def batch_create(self, request):
        items = request.data.get('items', [])
        created = []
        for item in items:
            obj, _ = Favorite.objects.get_or_create(user=request.user, content_type=item['content_type'], content_id=item['content_id'])
            created.append(obj.id)
        return Response({'success': True, 'created_ids': created})
    @extend_schema(summary="批量删除收藏", request=None, responses={204: OpenApiResponse(description="删除成功")})
    @action(detail=False, methods=['delete'], url_path='batch-delete')
    def batch_delete(self, request):
        ids = request.data.get('ids', [])
        Favorite.objects.filter(id__in=ids, user=request.user).delete()
        return Response({'success': True, 'message': '批量删除成功'})

@extend_schema(tags=["用户行为统计"], summary="用户行为统计", description="只读，返回用户行为聚合数据。")
class UserBehaviorStatsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserBehaviorStats.objects.all()
    serializer_class = UserBehaviorStatsSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return UserBehaviorStats.objects.filter(user=self.request.user)
    @extend_schema(summary="用户总播放时长", responses={200: OpenApiResponse(description="总播放时长(秒)")})
    @action(detail=False, methods=['get'], url_path='total-play-time')
    def total_play_time(self, request):
        total = self.get_queryset().aggregate(total=Sum('total_play_time'))['total'] or 0
        return Response({'total_play_time': total})

@extend_schema(tags=["内容互动统计"], summary="内容互动统计", description="只读，返回内容互动聚合数据。")
class ContentInteractionStatsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ContentInteractionStats.objects.all()
    serializer_class = ContentInteractionStatsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    @extend_schema(summary="内容总点赞数", parameters=[OpenApiParameter('content_type', str), OpenApiParameter('content_id', int)], responses={200: OpenApiResponse(description="总点赞数")})
    @action(detail=False, methods=['get'], url_path='total-likes')
    def total_likes(self, request):
        content_type = request.query_params.get('content_type')
        content_id = request.query_params.get('content_id')
        qs = self.get_queryset().filter(content_type=content_type, content_id=content_id)
        total = qs.aggregate(total=Sum('like_count'))['total'] or 0
        return Response({'total_likes': total})

@extend_schema(tags=["用户画像"], summary="用户画像API", description="获取和更新用户画像信息。", examples=[
    {
        "id": 1,
        "user": 1,
        "age_group": "25-34",
        "interest_categories": {"tech": 0.8, "finance": 0.6},
        "preferred_content_length": "medium",
        "preferred_time_slots": ["morning", "evening"],
        "active_days": [1,2,3,4,5],
        "device_preference": "mobile",
        "content_freshness_preference": 0.7,
        "diversity_preference": 0.5,
        "interaction_frequency": "high",
        "social_activity_level": "commenter",
        "news_reading_speed": "fast",
        "sentiment_preference": "positive",
        "last_updated_at": "2024-07-20T10:00:00Z",
        "created_at": "2024-07-01T10:00:00Z"
    }
])
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)
    @extend_schema(summary="获取当前用户画像", responses={200: UserProfileSerializer})
    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        return Response(UserProfileSerializer(profile).data)
    @extend_schema(summary="自动更新用户画像", description="根据用户行为自动更新画像（Mock实现）", responses={200: UserProfileSerializer}, examples=[{"success": true, "message": "画像已自动更新"}])
    @action(detail=False, methods=['post'], url_path='auto-update')
    def auto_update(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        # Mock: 随机调整兴趣权重
        if not profile.interest_categories:
            profile.interest_categories = {"tech": 0.5, "entertainment": 0.5}
        else:
            for k in profile.interest_categories:
                profile.interest_categories[k] = min(1.0, max(0.0, profile.interest_categories[k] + random.uniform(-0.1, 0.1)))
        profile.save()
        return Response({"success": True, "message": "画像已自动更新", "profile": UserProfileSerializer(profile).data})

@extend_schema(tags=["推荐"], summary="推荐API", description="个性化推荐、协同过滤、内容推荐、实时推荐等。", examples=[
    {
        "id": 1,
        "user": 1,
        "content_type": "audio",
        "content_id": 101,
        "algorithm_type": "collaborative",
        "recommendation_score": 0.95,
        "confidence_score": 0.88,
        "reasons": ["similar_users_liked"],
        "context_info": {"scene": "home"},
        "position_in_list": 1,
        "list_type": "home_feed",
        "is_viewed": False,
        "is_clicked": False,
        "is_played": False,
        "is_liked": False,
        "is_shared": False,
        "interaction_time": None,
        "session_id": "abc123",
        "created_at": "2024-07-20T10:00:00Z"
    }
])
class RecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Recommendation.objects.filter(user=self.request.user)
    @extend_schema(summary="获取个性化推荐（Mock）", parameters=[OpenApiParameter('algorithm_type', str)], responses={200: RecommendationSerializer(many=True)},
        examples=[{"id": 1, "content_type": "audio", "algorithm_type": "collaborative", "recommendation_score": 0.95}])
    @action(detail=False, methods=['get'], url_path='personalized')
    def personalized(self, request):
        algo = request.query_params.get('algorithm_type', 'collaborative')
        # Mock: 随机生成推荐内容
        mock_data = [
            {
                "id": i,
                "user": request.user.id,
                "content_type": random.choice(["audio", "video", "news"]),
                "content_id": 100 + i,
                "algorithm_type": algo,
                "recommendation_score": round(random.uniform(0.7, 1.0), 4),
                "confidence_score": round(random.uniform(0.7, 1.0), 4),
                "reasons": ["mock_reason"],
                "context_info": {"scene": "home"},
                "position_in_list": i,
                "list_type": "home_feed",
                "is_viewed": False,
                "is_clicked": False,
                "is_played": False,
                "is_liked": False,
                "is_shared": False,
                "interaction_time": None,
                "session_id": "mock_session",
                "created_at": "2024-07-20T10:00:00Z"
            } for i in range(1, 11)
        ]
        return Response(mock_data)
    @extend_schema(summary="获取AI推荐（Mock）", responses={200: RecommendationSerializer(many=True)},
        examples=[{"id": 1, "content_type": "audio", "algorithm_type": "ai", "recommendation_score": 0.98}])
    @action(detail=False, methods=['get'], url_path='ai')
    def ai(self, request):
        # Mock: AI推荐逻辑
        mock_data = [
            {
                "id": i,
                "user": request.user.id,
                "content_type": "audio",
                "content_id": 200 + i,
                "algorithm_type": "ai",
                "recommendation_score": round(random.uniform(0.8, 1.0), 4),
                "confidence_score": round(random.uniform(0.8, 1.0), 4),
                "reasons": ["ai_model"],
                "context_info": {"ai": "gpt-4o"},
                "position_in_list": i,
                "list_type": "ai_feed",
                "is_viewed": False,
                "is_clicked": False,
                "is_played": False,
                "is_liked": False,
                "is_shared": False,
                "interaction_time": None,
                "session_id": "ai_session",
                "created_at": "2024-07-20T10:00:00Z"
            } for i in range(1, 6)
        ]
        return Response(mock_data)
    @extend_schema(summary="获取协同过滤推荐（Mock）", responses={200: RecommendationSerializer(many=True)},
        examples=[{"id": 1, "content_type": "news", "algorithm_type": "collaborative", "recommendation_score": 0.92}])
    @action(detail=False, methods=['get'], url_path='collaborative')
    def collaborative(self, request):
        # Mock: 协同过滤推荐
        mock_data = [
            {
                "id": i,
                "user": request.user.id,
                "content_type": "news",
                "content_id": 300 + i,
                "algorithm_type": "collaborative",
                "recommendation_score": round(random.uniform(0.7, 0.95), 4),
                "confidence_score": round(random.uniform(0.7, 0.95), 4),
                "reasons": ["user_similarity"],
                "context_info": {"cf": "user-user"},
                "position_in_list": i,
                "list_type": "cf_feed",
                "is_viewed": False,
                "is_clicked": False,
                "is_played": False,
                "is_liked": False,
                "is_shared": False,
                "interaction_time": None,
                "session_id": "cf_session",
                "created_at": "2024-07-20T10:00:00Z"
            } for i in range(1, 6)
        ]
        return Response(mock_data)
    @extend_schema(summary="推荐内容统计", responses={200: OpenApiResponse(description="推荐内容统计")})
    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        total = self.get_queryset().count()
        avg_score = self.get_queryset().aggregate(avg=Avg('recommendation_score'))['avg'] or 0
        return Response({'total_recommendations': total, 'avg_score': avg_score})

@extend_schema(tags=["热点趋势"], summary="热点趋势API", description="获取当前热门话题及趋势分析。", examples=[
    {
        "id": 1,
        "keyword": "AI大模型",
        "category": "科技",
        "trend_type": "hot",
        "mention_count": 1200,
        "search_count": 800,
        "engagement_score": 0.95,
        "velocity_score": 0.8,
        "related_news_count": 30,
        "geographic_scope": "national",
        "age_group_distribution": {"18-24": 0.3, "25-34": 0.5},
        "peak_time": "10:00:00",
        "trend_start_time": "2024-07-19T08:00:00Z",
        "trend_end_time": None,
        "related_keywords": ["AI", "大模型", "GPT"],
        "sentiment_distribution": {"positive": 0.7, "neutral": 0.2, "negative": 0.1},
        "is_active": True,
        "created_at": "2024-07-19T08:00:00Z",
        "updated_at": "2024-07-20T10:00:00Z"
    }
])
class TrendingTopicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TrendingTopic.objects.filter(is_active=True)
    serializer_class = TrendingTopicSerializer
    permission_classes = [permissions.AllowAny]
    @extend_schema(summary="获取当前热点趋势（Mock分析）", responses={200: TrendingTopicSerializer(many=True)},
        examples=[{"keyword": "AI大模型", "trend_type": "hot", "engagement_score": 0.95}])
    @action(detail=False, methods=['get'], url_path='current')
    def current(self, request):
        # Mock: 随机生成热点趋势
        mock_data = [
            {
                "id": i,
                "keyword": random.choice(["AI大模型", "新能源", "世界杯", "奥运会", "元宇宙"]),
                "category": random.choice(["科技", "体育", "财经", "娱乐"]),
                "trend_type": random.choice(["hot", "rising", "breaking"]),
                "mention_count": random.randint(500, 2000),
                "search_count": random.randint(200, 1000),
                "engagement_score": round(random.uniform(0.7, 1.0), 2),
                "velocity_score": round(random.uniform(0.5, 1.0), 2),
                "related_news_count": random.randint(10, 50),
                "geographic_scope": "national",
                "age_group_distribution": {"18-24": 0.3, "25-34": 0.5},
                "peak_time": "10:00:00",
                "trend_start_time": "2024-07-19T08:00:00Z",
                "trend_end_time": None,
                "related_keywords": ["AI", "大模型", "GPT"],
                "sentiment_distribution": {"positive": 0.7, "neutral": 0.2, "negative": 0.1},
                "is_active": True,
                "created_at": "2024-07-19T08:00:00Z",
                "updated_at": "2024-07-20T10:00:00Z"
            } for i in range(1, 6)
        ]
        return Response(mock_data)
    @extend_schema(summary="趋势统计（Mock分析）", responses={200: OpenApiResponse(description="趋势统计")},
        examples=[{"total_trending": 5, "max_engagement_score": 0.98}])
    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        # Mock: 统计分析
        total = 5
        max_engagement = 0.98
        return Response({'total_trending': total, 'max_engagement_score': max_engagement}) 