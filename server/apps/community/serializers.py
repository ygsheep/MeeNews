from rest_framework import serializers
from .models import Comment, Like, Share, Report, PlayHistory, Favorite, UserBehaviorStats, ContentInteractionStats, UserProfile, Recommendation, TrendingTopic

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Share
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

class PlayHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayHistory
        fields = '__all__'

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'

class UserBehaviorStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBehaviorStats
        fields = '__all__'

class ContentInteractionStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentInteractionStats
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = '__all__'

class TrendingTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrendingTopic
        fields = '__all__'

class BatchDeleteRequestSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField(), help_text="要删除的ID列表")

class BatchFavoriteCreateRequestSerializer(serializers.Serializer):
    items = serializers.ListField(child=serializers.DictField(), help_text="批量收藏内容项")

class TotalPlayDurationResponseSerializer(serializers.Serializer):
    total_play_duration = serializers.IntegerField()

class TotalLikesResponseSerializer(serializers.Serializer):
    total_likes = serializers.IntegerField() 