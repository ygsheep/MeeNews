from rest_framework import serializers
from .models import AICommentary, AIAudioContent, AIVideoContent

class AICommentarySerializer(serializers.ModelSerializer):
    """AI解说内容序列化器"""
    class Meta:
        model = AICommentary
        fields = '__all__'

class AIAudioContentSerializer(serializers.ModelSerializer):
    """AI音频内容序列化器"""
    class Meta:
        model = AIAudioContent
        fields = '__all__'

class AIVideoContentSerializer(serializers.ModelSerializer):
    """AI视频内容序列化器"""
    class Meta:
        model = AIVideoContent
        fields = '__all__' 