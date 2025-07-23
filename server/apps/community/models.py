from django.db import models
from apps.users.models import User

class Comment(models.Model):
    """评论表，支持嵌套回复、表情、举报"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.CharField(max_length=20)  # news/audio/video
    content_id = models.BigIntegerField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    reply_to_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='replied_comments')
    like_count = models.IntegerField(default=0)
    reply_count = models.IntegerField(default=0)
    is_pinned = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    sentiment_score = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    emoji = models.CharField(max_length=20, blank=True, null=True)  # 支持表情
    is_reported = models.BooleanField(default=False)  # 是否被举报
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}"

class Like(models.Model):
    """点赞/点踩表，支持内容和评论"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    target_type = models.CharField(max_length=20)  # news/audio/video/comment
    target_id = models.BigIntegerField()
    is_like = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'target_type', 'target_id')
    def __str__(self):
        return f"{self.user.username} {'点赞' if self.is_like else '点踩'} {self.target_type}:{self.target_id}"

class Share(models.Model):
    """分享表"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.CharField(max_length=20)
    content_id = models.BigIntegerField()
    share_platform = models.CharField(max_length=20)
    share_text = models.TextField(blank=True, null=True)
    share_image_url = models.URLField(max_length=500, blank=True, null=True)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    device_info = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} 分享 {self.content_type}:{self.content_id}" 

class Report(models.Model):
    """举报表，支持举报评论、内容等"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    target_type = models.CharField(max_length=20)  # news/audio/video/comment
    target_id = models.BigIntegerField()
    reason = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default='pending')  # pending/approved/rejected
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)
    reviewed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='reviewed_reports')
    def __str__(self):
        return f"{self.user.username} 举报 {self.target_type}:{self.target_id}"

class PlayHistory(models.Model):
    """播放历史表，记录用户播放行为"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.CharField(max_length=20)  # audio/video
    content_id = models.BigIntegerField()
    play_duration = models.IntegerField(default=0)  # 实际播放时长(秒)
    total_duration = models.IntegerField(default=0)  # 内容总时长(秒)
    completion_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # 0-100
    play_source = models.CharField(max_length=20, default='home')
    device_type = models.CharField(max_length=20, blank=True, null=True)
    device_info = models.JSONField(blank=True, null=True)
    play_speed = models.DecimalField(max_digits=3, decimal_places=1, default=1.0)
    quality = models.CharField(max_length=20, blank=True, null=True)
    network_type = models.CharField(max_length=20, blank=True, null=True)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    location_info = models.JSONField(blank=True, null=True)
    session_id = models.CharField(max_length=64, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} 播放 {self.content_type}:{self.content_id}"

class Favorite(models.Model):
    """收藏表，支持多类型内容收藏"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.CharField(max_length=20)  # news/audio/video/topic
    content_id = models.BigIntegerField()
    folder_name = models.CharField(max_length=50, default='默认收藏夹')
    tags = models.JSONField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('user', 'content_type', 'content_id')
    def __str__(self):
        return f"{self.user.username} 收藏 {self.content_type}:{self.content_id}"

class UserBehaviorStats(models.Model):
    """用户行为统计表，按天统计"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    total_play_time = models.IntegerField(default=0)
    total_play_count = models.IntegerField(default=0)
    audio_play_time = models.IntegerField(default=0)
    video_play_time = models.IntegerField(default=0)
    favorite_count = models.IntegerField(default=0)
    share_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    search_count = models.IntegerField(default=0)
    active_hours = models.JSONField(blank=True, null=True)
    preferred_categories = models.JSONField(blank=True, null=True)
    avg_completion_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('user', 'date')
    def __str__(self):
        return f"{self.user.username} {self.date} 行为统计"

class ContentInteractionStats(models.Model):
    """内容互动统计表，按天统计"""
    content_type = models.CharField(max_length=20)  # news/audio/video
    content_id = models.BigIntegerField()
    date = models.DateField()
    play_count = models.IntegerField(default=0)
    unique_play_count = models.IntegerField(default=0)
    total_play_time = models.IntegerField(default=0)
    avg_play_time = models.IntegerField(default=0)
    completion_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    share_count = models.IntegerField(default=0)
    favorite_count = models.IntegerField(default=0)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    bounce_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    retention_rate = models.JSONField(blank=True, null=True)
    traffic_source = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('content_type', 'content_id', 'date')
    def __str__(self):
        return f"{self.content_type}:{self.content_id} {self.date} 互动统计" 

class UserProfile(models.Model):
    """用户画像表，存储用户兴趣、偏好等画像信息"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age_group = models.CharField(max_length=20, default='unknown')
    interest_categories = models.JSONField(blank=True, null=True)
    preferred_content_length = models.CharField(max_length=20, default='mixed')
    preferred_time_slots = models.JSONField(blank=True, null=True)
    active_days = models.JSONField(blank=True, null=True)
    device_preference = models.CharField(max_length=20, default='mobile')
    content_freshness_preference = models.DecimalField(max_digits=3, decimal_places=2, default=0.7)
    diversity_preference = models.DecimalField(max_digits=3, decimal_places=2, default=0.5)
    interaction_frequency = models.CharField(max_length=20, default='medium')
    social_activity_level = models.CharField(max_length=20, default='lurker')
    news_reading_speed = models.CharField(max_length=20, default='normal')
    sentiment_preference = models.CharField(max_length=20, default='mixed')
    last_updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} 画像"

class Recommendation(models.Model):
    """推荐记录表，记录每次推荐的内容及算法"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.CharField(max_length=20)  # news/audio/video/topic
    content_id = models.BigIntegerField()
    algorithm_type = models.CharField(max_length=20)  # collaborative/content_based/trending/social/location/time_based
    recommendation_score = models.DecimalField(max_digits=5, decimal_places=4)
    confidence_score = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    reasons = models.JSONField(blank=True, null=True)
    context_info = models.JSONField(blank=True, null=True)
    position_in_list = models.IntegerField(blank=True, null=True)
    list_type = models.CharField(max_length=20, default='home_feed')
    is_viewed = models.BooleanField(default=False)
    is_clicked = models.BooleanField(default=False)
    is_played = models.BooleanField(default=False)
    is_liked = models.BooleanField(default=False)
    is_shared = models.BooleanField(default=False)
    interaction_time = models.DateTimeField(blank=True, null=True)
    session_id = models.CharField(max_length=64, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} 推荐 {self.content_type}:{self.content_id}"

class TrendingTopic(models.Model):
    """热点趋势表，记录当前热门话题及趋势分析"""
    keyword = models.CharField(max_length=100)
    category = models.CharField(max_length=50, blank=True, null=True)
    trend_type = models.CharField(max_length=20)  # breaking/rising/hot/persistent
    mention_count = models.IntegerField(default=0)
    search_count = models.IntegerField(default=0)
    engagement_score = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    velocity_score = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    related_news_count = models.IntegerField(default=0)
    geographic_scope = models.CharField(max_length=20, default='national')
    age_group_distribution = models.JSONField(blank=True, null=True)
    peak_time = models.TimeField(blank=True, null=True)
    trend_start_time = models.DateTimeField(blank=True, null=True)
    trend_end_time = models.DateTimeField(blank=True, null=True)
    related_keywords = models.JSONField(blank=True, null=True)
    sentiment_distribution = models.JSONField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.keyword} 热点趋势" 