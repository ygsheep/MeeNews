from django.db import models
from apps.content.models import RawNews
from apps.users.models import User

class AICommentary(models.Model):
    """AI解说内容表"""
    raw_news = models.ForeignKey(RawNews, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    script = models.TextField()
    summary = models.CharField(max_length=1000, blank=True, null=True)
    commentary_style = models.CharField(max_length=20, choices=[('news','新闻'),('casual','闲聊'),('humorous','幽默'),('professional','专业'),('emotional','情感')], default='news')
    target_duration = models.IntegerField(blank=True, null=True)
    voice_type = models.CharField(max_length=50, default='standard_female')
    language = models.CharField(max_length=10, default='zh-CN')
    generation_model = models.CharField(max_length=50, blank=True, null=True)
    generation_prompt = models.TextField(blank=True, null=True)
    quality_score = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    is_reviewed = models.BooleanField(default=False)
    reviewed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='reviewed_commentaries')
    reviewed_at = models.DateTimeField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

class AIAudioContent(models.Model):
    """AI音频内容表"""
    commentary = models.ForeignKey(AICommentary, on_delete=models.CASCADE)
    audio_url = models.URLField(max_length=500)
    duration = models.IntegerField()
    file_size = models.BigIntegerField(blank=True, null=True)
    bitrate = models.IntegerField(blank=True, null=True)
    format = models.CharField(max_length=10, default='mp3')
    voice_type = models.CharField(max_length=50)
    speech_rate = models.DecimalField(max_digits=3, decimal_places=1, default=1.0)
    tts_service = models.CharField(max_length=50, blank=True, null=True)
    generation_time = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    play_count = models.BigIntegerField(default=0)
    like_count = models.IntegerField(default=0)
    share_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"音频: {self.commentary.title}"

class AIVideoContent(models.Model):
    """AI视频内容表"""
    commentary = models.ForeignKey(AICommentary, on_delete=models.CASCADE)
    video_url = models.URLField(max_length=500)
    thumbnail_url = models.URLField(max_length=500, blank=True, null=True)
    duration = models.IntegerField()
    file_size = models.BigIntegerField(blank=True, null=True)
    resolution = models.CharField(max_length=20, blank=True, null=True)
    format = models.CharField(max_length=10, default='mp4')
    avatar_type = models.CharField(max_length=50, blank=True, null=True)
    background_style = models.CharField(max_length=50, blank=True, null=True)
    generation_service = models.CharField(max_length=50, blank=True, null=True)
    generation_time = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    play_count = models.BigIntegerField(default=0)
    like_count = models.IntegerField(default=0)
    share_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"视频: {self.commentary.title}"
