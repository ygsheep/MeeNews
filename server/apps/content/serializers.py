from rest_framework import serializers
from .models import NewsCategory, RawNews, ContentTag, ContentTagRelation, ContentModeration, ContentInteractionStats
from django.contrib.contenttypes.models import ContentType
from .models import VideoContent

class VideoContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoContent
        fields = [
            'id', 'title', 'description', 'source', 'source_url', 'video_url', 'duration',
            'quality_level', 'published_at', 'keywords', 'created_at', 'updated_at'
        ]

class NewsCategorySerializer(serializers.ModelSerializer):
    """资讯分类序列化器，支持递归children"""
    children = serializers.SerializerMethodField()
    class Meta:
        model = NewsCategory
        fields = ['id', 'name', 'name_en', 'description', 'icon_url', 'color_code', 'children']
    def get_children(self, obj):
        return NewsCategorySerializer(obj.children.all(), many=True).data

class RawNewsSerializer(serializers.ModelSerializer):
    """原始新闻内容序列化器"""
    video_content = serializers.SerializerMethodField()
    class Meta:
        model = RawNews
        fields = '__all__'
    def get_video_content(self, obj):
        if obj.type == 'video' and obj.source_url:
            video = VideoContent.objects.filter(source_url=obj.source_url).first()
            if video:
                return VideoContentSerializer(video).data
        return None

class ContentTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentTag
        fields = '__all__'

class ContentTagRelationSerializer(serializers.ModelSerializer):
    content_type = serializers.SlugRelatedField(slug_field='model', queryset=ContentType.objects.all())
    tag = serializers.SlugRelatedField(slug_field='name', queryset=ContentTag.objects.all())
    class Meta:
        model = ContentTagRelation
        fields = ['id', 'content_type', 'object_id', 'tag', 'relevance_score', 'is_auto_tagged', 'created_at']

class ContentModerationSerializer(serializers.ModelSerializer):
    content_type = serializers.SlugRelatedField(slug_field='model', queryset=ContentType.objects.all())
    moderator = serializers.StringRelatedField()
    class Meta:
        model = ContentModeration
        fields = '__all__'

class ContentInteractionStatsSerializer(serializers.ModelSerializer):
    content_type = serializers.SlugRelatedField(slug_field='model', queryset=ContentType.objects.all())
    class Meta:
        model = ContentInteractionStats
        fields = '__all__' 