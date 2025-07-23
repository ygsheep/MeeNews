from django.urls import path
from .views import NewsCategoryListView, ContentRecommendView, ContentDetailView, ContentSearchView, ContentTagListView, ContentTagRelationView, ContentModerationView, ContentStatsView, ContentViewSet, ContentPublicListView, ContentTrendingView, SearchSuggestionsView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'content', ContentViewSet, basename='content')

urlpatterns = router.urls + [
    path('categories', NewsCategoryListView.as_view()),  # 分类列表
    path('content/recommend', ContentRecommendView.as_view()),  # 推荐内容
    path('content/public', ContentPublicListView.as_view()),  # 公开内容列表
    path('content/trending', ContentTrendingView.as_view()),  # 热门内容
    path('search/suggestions', SearchSuggestionsView.as_view()),  # 搜索建议
    path('content/<int:id>', ContentDetailView.as_view()),  # 内容详情
    path('content/search', ContentSearchView.as_view()),  # 内容搜索
    path('content/tags', ContentTagListView.as_view()),  # 标签列表与创建
    path('content/<int:id>/tags', ContentTagRelationView.as_view()),  # 内容打标签/获取标签
    path('content/<int:id>/moderation', ContentModerationView.as_view()),  # 内容审核
    path('content/<int:content_id>/stats', ContentStatsView.as_view()),  # 内容统计
] 