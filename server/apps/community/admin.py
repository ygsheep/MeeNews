from django.contrib import admin
from .models import Comment, Like, Share, Report, PlayHistory, Favorite, UserBehaviorStats, ContentInteractionStats, UserProfile, Recommendation, TrendingTopic

admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Share)
admin.site.register(Report)
admin.site.register(PlayHistory)
admin.site.register(Favorite)
admin.site.register(UserBehaviorStats)
admin.site.register(ContentInteractionStats)
admin.site.register(UserProfile)
admin.site.register(Recommendation)
admin.site.register(TrendingTopic) 