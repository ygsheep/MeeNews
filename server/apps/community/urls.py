from rest_framework.routers import DefaultRouter
from .views import CommentViewSet, LikeViewSet, ShareViewSet, ReportViewSet, PlayHistoryViewSet, FavoriteViewSet, UserBehaviorStatsViewSet, ContentInteractionStatsViewSet, UserProfileViewSet, RecommendationViewSet, TrendingTopicViewSet

router = DefaultRouter()
router.register(r'comments', CommentViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'shares', ShareViewSet)
router.register(r'reports', ReportViewSet)
router.register(r'play-history', PlayHistoryViewSet)
router.register(r'favorites', FavoriteViewSet)
router.register(r'user-behavior-stats', UserBehaviorStatsViewSet)
router.register(r'content-interaction-stats', ContentInteractionStatsViewSet)
router.register(r'user-profiles', UserProfileViewSet)
router.register(r'recommendations', RecommendationViewSet)
router.register(r'trending-topics', TrendingTopicViewSet)

urlpatterns = router.urls 