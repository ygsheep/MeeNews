from rest_framework import generics, viewsets, filters, status, permissions
from .models import NewsCategory, RawNews, ContentTag, ContentTagRelation, ContentModeration, ContentInteractionStats
from .serializers import NewsCategorySerializer, RawNewsSerializer, ContentTagSerializer, ContentTagRelationSerializer, ContentModerationSerializer, ContentInteractionStatsSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.db import transaction
from .permissions import IsAuthorOrAdmin, IsAdminOrReadOnly
from rest_framework.decorators import action
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import RawNews, NewsCategory
from .serializers import RawNewsSerializer
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample
import datetime
from django.utils import timezone

# 统一响应格式工具
def api_response(success=True, code=200, message="Success", data=None):
    return Response({
        "success": success,
        "code": code,
        "message": message,
        "data": data if data is not None else {},
        "timestamp": timezone.now().isoformat()
    }, status=code)

class NewsCategoryListView(generics.ListAPIView):
    """
    分类列表API
    """
    queryset = NewsCategory.objects.filter(parent=None, is_active=True)
    serializer_class = NewsCategorySerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return api_response(success=True, code=200, message="Success", data=serializer.data)

class ContentRecommendView(generics.ListAPIView):
    """
    内容推荐API，支持多媒体类型、分类、标签筛选
    """
    serializer_class = RawNewsSerializer
    pagination_class = PageNumberPagination
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = RawNews.objects.filter(is_processed=True)
        type_param = self.request.query_params.get('type')
        if type_param:
            queryset = queryset.filter(type=type_param)
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        tag = self.request.query_params.get('tag')
        if tag:
            queryset = queryset.filter(tags__contains=[tag])
        sort = self.request.query_params.get('sort', 'published_at')
        if sort == 'hot':
            queryset = queryset.order_by('-importance_score')
        elif sort == 'popular':
            queryset = queryset.order_by('-sentiment_score')
        else:
            queryset = queryset.order_by('-published_at')
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True) if page is not None else self.get_serializer(queryset, many=True)
        data = serializer.data
        pagination = None
        if page is not None:
            pagination = {
                "page": self.paginator.page.number,
                "page_size": self.paginator.get_page_size(request),
                "total": self.paginator.page.paginator.count,
                "total_pages": self.paginator.page.paginator.num_pages,
                "has_next": self.paginator.page.has_next(),
                "has_previous": self.paginator.page.has_previous(),
            }
        return api_response(
            success=True,
            code=200,
            message="Success",
            data={"results": data, "pagination": pagination} if pagination else {"results": data}
        )

class ContentDetailView(generics.RetrieveAPIView):
    """
    内容详情API
    """
    queryset = RawNews.objects.all()
    serializer_class = RawNewsSerializer
    lookup_field = 'id'
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_response(success=True, code=200, message="Success", data=serializer.data)

class ContentSearchView(generics.ListAPIView):
    """
    内容搜索API，支持多媒体类型、分类、标签筛选
    """
    serializer_class = RawNewsSerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content', 'summary']
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = RawNews.objects.filter(is_processed=True)
        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(title__icontains=q)
        type_param = self.request.query_params.get('type')
        if type_param:
            queryset = queryset.filter(type=type_param)
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        tag = self.request.query_params.get('tag')
        if tag:
            queryset = queryset.filter(tags__contains=[tag])
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True) if page is not None else self.get_serializer(queryset, many=True)
        data = serializer.data
        pagination = None
        if page is not None:
            pagination = {
                "page": self.paginator.page.number,
                "page_size": self.paginator.get_page_size(request),
                "total": self.paginator.page.paginator.count,
                "total_pages": self.paginator.page.paginator.num_pages,
                "has_next": self.paginator.page.has_next(),
                "has_previous": self.paginator.page.has_previous(),
            }
        return api_response(
            success=True,
            code=200,
            message="Success",
            data={"results": data, "pagination": pagination} if pagination else {"results": data}
        )

class ContentTagListView(generics.ListCreateAPIView):
    """内容标签列表与创建API"""
    queryset = ContentTag.objects.filter(is_active=True)
    serializer_class = ContentTagSerializer
    permission_classes = [IsAdminOrReadOnly]

class ContentTagRelationView(APIView):
    """内容标签关联API，支持打标签和获取标签"""
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, id):
        # 批量打标签
        tags = request.data.get('tags')
        content_type_str = request.data.get('content_type')
        if not content_type_str or not tags or not isinstance(tags, list):
            return Response({"success": False, "message": "content_type和tags(数组)为必填"}, status=status.HTTP_400_BAD_REQUEST)
        content_type = get_object_or_404(ContentType, model=content_type_str)
        obj = content_type.get_object_for_this_type(pk=id)
        # 权限校验
        if not (request.user.is_staff or getattr(obj, 'author', None) == request.user):
            return Response({"success": False, "message": "无权限"}, status=status.HTTP_403_FORBIDDEN)
        created_tags = []
        for tag_name in tags:
            tag = get_object_or_404(ContentTag, name=tag_name)
            relation, created = ContentTagRelation.objects.get_or_create(
                content_type=content_type, object_id=id, tag=tag,
                defaults={"relevance_score": request.data.get('relevance_score', 1.0), "is_auto_tagged": request.data.get('is_auto_tagged', False)}
            )
            if created:
                tag.usage_count = ContentTagRelation.objects.filter(tag=tag).count()
                tag.save()
                created_tags.append(ContentTagRelationSerializer(relation).data)
        return Response({"success": True, "data": created_tags})
    def get(self, request, id):
        # 获取内容所有标签
        content_type_str = request.query_params.get('content_type')
        if not content_type_str:
            return Response({"success": False, "message": "content_type为必填"}, status=status.HTTP_400_BAD_REQUEST)
        content_type = get_object_or_404(ContentType, model=content_type_str)
        relations = ContentTagRelation.objects.filter(content_type=content_type, object_id=id)
        return Response({"success": True, "data": ContentTagRelationSerializer(relations, many=True).data})

class ContentModerationView(APIView):
    """内容审核API，支持提交审核和获取审核历史"""
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request, id):
        content_type_str = request.query_params.get('content_type')
        if not content_type_str:
            return Response({"success": False, "message": "content_type为必填"}, status=status.HTTP_400_BAD_REQUEST)
        content_type = get_object_or_404(ContentType, model=content_type_str)
        moderations = ContentModeration.objects.filter(content_type=content_type, object_id=id).order_by('-created_at')
        return Response({"success": True, "data": ContentModerationSerializer(moderations, many=True).data})
    @transaction.atomic
    def post(self, request, id):
        content_type_str = request.data.get('content_type')
        status_val = request.data.get('status')
        if not content_type_str or not status_val:
            return Response({"success": False, "message": "content_type和status为必填"}, status=status.HTTP_400_BAD_REQUEST)
        content_type = get_object_or_404(ContentType, model=content_type_str)
        obj = content_type.get_object_for_this_type(pk=id)
        moderation = ContentModeration.objects.create(
            content_type=content_type,
            object_id=id,
            status=status_val,
            moderator=request.user if request.user.is_authenticated else None,
            moderation_reason=request.data.get('moderation_reason'),
            ai_score=request.data.get('ai_score'),
            ai_flags=request.data.get('ai_flags'),
            user_reports_count=request.data.get('user_reports_count', 0)
        )
        return Response({"success": True, "data": ContentModerationSerializer(moderation).data})

class ContentStatsView(APIView):
    """内容统计API，支持获取总计和按天统计"""
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, content_id):
        content_type_str = request.query_params.get('content_type')
        if not content_type_str:
            return Response({"success": False, "message": "content_type为必填"}, status=status.HTTP_400_BAD_REQUEST)
        content_type = get_object_or_404(ContentType, model=content_type_str)
        # 总计
        total = ContentInteractionStats.objects.filter(content_type=content_type, object_id=content_id, date__isnull=True).first()
        # 按天
        daily = ContentInteractionStats.objects.filter(content_type=content_type, object_id=content_id, date__isnull=False).order_by('date')
        return Response({
            "success": True,
            "data": {
                "total": ContentInteractionStatsSerializer(total).data if total else None,
                "daily": ContentInteractionStatsSerializer(daily, many=True).data
            }
        })

class CategoryContentPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class ContentViewSet(viewsets.ReadOnlyModelViewSet):
    # ... existing code ...
    def get_queryset(self):
        queryset = RawNews.objects.all()
        type_param = self.request.query_params.get('type')
        if type_param:
            queryset = queryset.filter(type=type_param)
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        tag = self.request.query_params.get('tag')
        if tag:
            queryset = queryset.filter(tags__contains=[tag])
        return queryset

    @extend_schema(
        summary="根据分类获取内容",
        description="获取指定分类下的内容，支持分页、排序、时长筛选。",
        parameters=[
            OpenApiParameter('sort', str, description='排序方式(latest|popular|hot|duration)', required=False),
            OpenApiParameter('duration_min', int, description='最小时长(秒)', required=False),
            OpenApiParameter('duration_max', int, description='最大时长(秒)', required=False),
            OpenApiParameter('page', int, description='页码', required=False),
            OpenApiParameter('page_size', int, description='每页数量', required=False),
        ],
        responses={200: RawNewsSerializer(many=True)},
        examples=[
            OpenApiExample(
                '科技资讯内容示例',
                value={
                    "id": 101,
                    "title": "AI驱动的新闻推荐系统上线",
                    "content": "羊咩快报平台正式发布AI驱动的新闻推荐系统，提升用户个性化体验。",
                    "summary": "AI推荐系统助力个性化资讯推送。",
                    "author": "新闻编辑部",
                    "source_url": "https://news.yangmie.com/ai/101",
                    "image_urls": ["https://cdn.yangmie.com/images/ai-news-101.jpg"],
                    "published_at": "2025-07-20T10:00:00Z",
                    "category": 2,
                    "tags": ["AI", "推荐", "新闻"],
                    "keywords": ["人工智能", "个性化推荐", "新闻平台"],
                    "sentiment_score": 0.92,
                    "importance_score": 0.95,
                    "is_processed": True,
                    "is_duplicate": False,
                    "language": "zh-CN",
                    "created_at": "2025-07-20T10:00:00Z",
                    "updated_at": "2025-07-20T10:00:00Z"
                },
                response_only=True,
                description="真实业务场景下的科技资讯内容示例。"
            )
        ]
    )
    @action(detail=True, methods=['get'], url_path='category', url_name='category-content')
    def category_content(self, request, pk=None):
        """
        获取指定分类下的内容，支持分页、排序、时长筛选。
        GET /content/category/{category_id}/
        支持参数：sort, duration_min, duration_max, page, page_size
        """
        category = get_object_or_404(NewsCategory, pk=pk)
        queryset = RawNews.objects.filter(category=category)
        # 排序
        sort = request.query_params.get('sort', 'latest')
        if sort == 'popular':
            queryset = queryset.order_by('-importance_score')
        elif sort == 'hot':
            queryset = queryset.order_by('-sentiment_score')
        elif sort == 'duration':
            queryset = queryset.order_by('-duration') if hasattr(RawNews, 'duration') else queryset
        else:
            queryset = queryset.order_by('-published_at')
        # 时长筛选
        duration_min = request.query_params.get('duration_min')
        duration_max = request.query_params.get('duration_max')
        if duration_min and hasattr(RawNews, 'duration'):
            queryset = queryset.filter(duration__gte=int(duration_min))
        if duration_max and hasattr(RawNews, 'duration'):
            queryset = queryset.filter(duration__lte=int(duration_max))
        # 分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = RawNewsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = RawNewsSerializer(queryset, many=True)
        return Response(serializer.data)

class ContentPublicListView(generics.ListAPIView):
    """
    公开内容列表API
    GET /content/public
    支持分页、分类、type、sort
    """
    serializer_class = RawNewsSerializer
    pagination_class = PageNumberPagination
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = RawNews.objects.filter(is_processed=True)
        type_param = self.request.query_params.get('type')
        if type_param:
            queryset = queryset.filter(type=type_param)
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        sort = self.request.query_params.get('sort', 'latest')
        if sort == 'popular':
            queryset = queryset.order_by('-importance_score')
        elif sort == 'hot':
            queryset = queryset.order_by('-sentiment_score')
        elif sort == 'duration' and hasattr(RawNews, 'duration'):
            queryset = queryset.order_by('-duration')
        else:
            queryset = queryset.order_by('-published_at')
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True) if page is not None else self.get_serializer(queryset, many=True)
        data = serializer.data
        pagination = None
        if page is not None:
            pagination = {
                "page": self.paginator.page.number,
                "page_size": self.paginator.get_page_size(request),
                "total": self.paginator.page.paginator.count,
                "total_pages": self.paginator.page.paginator.num_pages,
                "has_next": self.paginator.page.has_next(),
                "has_previous": self.paginator.page.has_previous(),
            }
        return api_response(
            success=True,
            code=200,
            message="Success",
            data={"results": data, "pagination": pagination} if pagination else {"results": data}
        )

class ContentTrendingView(generics.ListAPIView):
    """
    热门内容API
    GET /content/trending
    支持 period, category_id, limit
    """
    serializer_class = RawNewsSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = RawNews.objects.filter(is_processed=True)
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        period = self.request.query_params.get('period', 'day')
        now = timezone.now()
        if period == 'day':
            since = now - datetime.timedelta(days=1)
        elif period == 'week':
            since = now - datetime.timedelta(weeks=1)
        elif period == 'month':
            since = now - datetime.timedelta(days=30)
        else:
            since = None
        if since:
            queryset = queryset.filter(published_at__gte=since)
        queryset = queryset.order_by('-importance_score', '-sentiment_score', '-published_at')
        return queryset

    def list(self, request, *args, **kwargs):
        limit = int(request.query_params.get('limit', 20))
        limit = min(limit, 100)
        queryset = self.get_queryset()[:limit]
        serializer = self.get_serializer(queryset, many=True)
        return api_response(success=True, code=200, message="Success", data={"results": serializer.data})

class SearchSuggestionsView(APIView):
    """
    搜索建议API
    GET /search/suggestions?q=xxx&limit=5
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        q = request.query_params.get('q', '').strip()
        limit = int(request.query_params.get('limit', 5))
        suggestions = []
        if q:
            # 标题建议
            title_qs = RawNews.objects.filter(title__icontains=q).values_list('title', flat=True).distinct()[:limit]
            for t in title_qs:
                suggestions.append({
                    "text": t,
                    "type": "title",
                    "highlight": t.replace(q, f"<em>{q}</em>") if q in t else t
                })
            # 标签建议
            tag_qs = RawNews.objects.filter(tags__icontains=q).values_list('tags', flat=True)
            tag_set = set()
            for tags in tag_qs:
                if tags:
                    for tag in tags:
                        if q in tag and tag not in tag_set:
                            tag_set.add(tag)
                            suggestions.append({
                                "text": tag,
                                "type": "tag",
                                "highlight": tag.replace(q, f"<em>{q}</em>")
                            })
                            if len(suggestions) >= limit:
                                break
                if len(suggestions) >= limit:
                    break
        return api_response(success=True, code=200, message="Success", data={"suggestions": suggestions[:limit]}) 