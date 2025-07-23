from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

class ContentCategory(models.Model):
    """内容分类表 - 支持多种内容类型"""
    CONTENT_TYPE_CHOICES = [
        ('all', '全部'),
        ('article', '文章'),
        ('video', '视频'),
        ('audio', '音频'),
        ('news', '资讯'),
    ]
    
    name = models.CharField(max_length=50, verbose_name='分类名称')
    name_en = models.CharField(max_length=50, blank=True, null=True, verbose_name='英文名称')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='URL标识')
    description = models.TextField(blank=True, null=True, verbose_name='分类描述')
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name='图标名称')
    icon_url = models.URLField(max_length=255, blank=True, null=True, verbose_name='图标链接')
    color_code = models.CharField(max_length=7, blank=True, null=True, verbose_name='主题色')
    cover_image = models.URLField(max_length=500, blank=True, null=True, verbose_name='封面图片')
    
    # 支持的内容类型
    supported_content_types = models.JSONField(default=list, verbose_name='支持的内容类型')
    
    # 层级关系
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, 
                              related_name='children', verbose_name='父分类')
    level = models.PositiveIntegerField(default=0, verbose_name='层级深度')
    
    # 排序和状态
    sort_order = models.IntegerField(default=0, verbose_name='排序权重')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    is_featured = models.BooleanField(default=False, verbose_name='是否推荐')
    
    # SEO和搜索
    keywords = models.JSONField(blank=True, null=True, verbose_name='关键词')
    meta_description = models.CharField(max_length=200, blank=True, null=True, verbose_name='SEO描述')
    
    # 统计信息
    content_count = models.PositiveIntegerField(default=0, verbose_name='内容数量')
    popularity_score = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='热度分值')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '内容分类'
        verbose_name_plural = '内容分类'
        ordering = ['sort_order', 'name']
    
    def __str__(self):
        return self.name
    
    def get_full_name(self):
        """获取完整分类路径"""
        if self.parent:
            return f"{self.parent.get_full_name()} > {self.name}"
        return self.name

# 保留原有NewsCategory用于兼容
class NewsCategory(ContentCategory):
    """资讯分类表 - 继承自ContentCategory用于兼容"""
    class Meta:
        proxy = True
        verbose_name = '资讯分类'
        verbose_name_plural = '资讯分类'

class RawNews(models.Model):
    """原始新闻内容表"""
    TYPE_CHOICES = [
        ('audio', '音频'),
        ('video', '视频'),
        ('article', '文章'),
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='article', verbose_name='内容类型')
    source = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=500)
    content = models.TextField()
    summary = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    source_url = models.URLField(max_length=500, unique=True)
    image_urls = models.JSONField(blank=True, null=True)
    published_at = models.DateTimeField()
    crawled_at = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=10, default='zh-CN')
    category = models.ForeignKey(NewsCategory, null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.JSONField(blank=True, null=True)
    keywords = models.JSONField(blank=True, null=True)
    sentiment_score = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    importance_score = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    is_processed = models.BooleanField(default=False)
    is_duplicate = models.BooleanField(default=False)
    duplicate_of = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='duplicates')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

class ContentTag(models.Model):
    """内容标签表 - 增强版标签系统"""
    TAG_TYPE_CHOICES = [
        ('general', '通用'),
        ('topic', '话题'),
        ('emotion', '情感'),
        ('category', '分类'),
        ('location', '地域'),
        ('person', '人物'),
        ('event', '事件'),
        ('technology', '技术'),
        ('trend', '趋势'),
    ]
    
    name = models.CharField(max_length=50, unique=True, verbose_name='标签名称')
    slug = models.SlugField(max_length=50, unique=True, default='temp-slug', verbose_name='URL标识')
    description = models.TextField(blank=True, null=True, verbose_name='标签描述')
    tag_type = models.CharField(max_length=20, choices=TAG_TYPE_CHOICES, default='general', verbose_name='标签类型')
    
    # 外观设置
    color_code = models.CharField(max_length=7, blank=True, null=True, verbose_name='标签颜色')
    background_color = models.CharField(max_length=7, blank=True, null=True, verbose_name='背景色')
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name='图标')
    
    # 分类关联
    category = models.ForeignKey(ContentCategory, null=True, blank=True, on_delete=models.SET_NULL,
                                related_name='tags', verbose_name='所属分类')
    
    # 支持的内容类型
    supported_content_types = models.JSONField(default=list, verbose_name='支持的内容类型')
    
    # 统计和权重
    usage_count = models.PositiveIntegerField(default=0, verbose_name='使用次数')
    content_count = models.PositiveIntegerField(default=0, verbose_name='关联内容数')
    popularity_score = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='热度分值')
    trending_score = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='趋势分值')
    
    # 状态管理
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    is_featured = models.BooleanField(default=False, verbose_name='是否推荐')
    is_trending = models.BooleanField(default=False, verbose_name='是否热门')
    is_auto_generated = models.BooleanField(default=False, verbose_name='是否自动生成')
    
    # SEO和搜索
    related_tags = models.ManyToManyField('self', blank=True, symmetrical=False, verbose_name='相关标签')
    synonyms = models.JSONField(blank=True, null=True, verbose_name='同义词')
    search_weight = models.DecimalField(max_digits=5, decimal_places=2, default=1.0, verbose_name='搜索权重')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '内容标签'
        verbose_name_plural = '内容标签'
        ordering = ['-popularity_score', 'name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['tag_type']),
            models.Index(fields=['popularity_score']),
            models.Index(fields=['is_trending']),
        ]
    
    def __str__(self):
        return self.name
    
    def increment_usage(self):
        """增加使用次数"""
        self.usage_count += 1
        self.save(update_fields=['usage_count'])

class Article(models.Model):
    """文章内容模型"""
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('pending', '待审核'),
        ('published', '已发布'),
        ('archived', '已归档'),
        ('deleted', '已删除'),
    ]
    
    QUALITY_CHOICES = [
        ('low', '一般'),
        ('medium', '良好'),
        ('high', '优质'),
        ('premium', '精品'),
    ]
    
    # 基本信息
    title = models.CharField(max_length=500, verbose_name='标题')
    subtitle = models.CharField(max_length=500, blank=True, null=True, verbose_name='副标题')
    content = models.TextField(verbose_name='文章正文')
    summary = models.CharField(max_length=1000, blank=True, null=True, verbose_name='摘要')
    word_count = models.PositiveIntegerField(default=0, verbose_name='字数')
    reading_time = models.PositiveIntegerField(default=0, verbose_name='预计阅读时间(分钟)')
    
    # 作者和来源
    author = models.CharField(max_length=100, blank=True, null=True, verbose_name='作者')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, 
                               on_delete=models.SET_NULL, related_name='created_articles', verbose_name='创建者')
    source = models.CharField(max_length=100, blank=True, null=True, verbose_name='来源')
    source_url = models.URLField(max_length=500, blank=True, null=True, verbose_name='原始链接')
    
    # 媒体文件
    cover_image = models.URLField(max_length=500, blank=True, null=True, verbose_name='封面图片')
    thumbnail_url = models.URLField(max_length=500, blank=True, null=True, verbose_name='缩略图')
    
    # 分类和标签
    category = models.ForeignKey(ContentCategory, null=True, blank=True, on_delete=models.SET_NULL,
                                related_name='articles', verbose_name='分类')
    tags = models.ManyToManyField(ContentTag, blank=True, verbose_name='标签')
    
    # TTS相关
    has_tts = models.BooleanField(default=False, verbose_name='是否支持语音播放')
    tts_url = models.URLField(max_length=500, blank=True, null=True, verbose_name='TTS音频链接')
    tts_duration = models.PositiveIntegerField(blank=True, null=True, verbose_name='TTS时长(秒)')
    
    # 文章结构
    table_of_contents = models.JSONField(blank=True, null=True, verbose_name='目录结构')
    sections = models.JSONField(blank=True, null=True, verbose_name='章节信息')
    
    # 格式和样式
    content_format = models.CharField(max_length=20, default='markdown', verbose_name='内容格式')
    reading_mode = models.CharField(max_length=20, default='normal', verbose_name='阅读模式')
    
    # 状态和质量
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='状态')
    quality_level = models.CharField(max_length=20, choices=QUALITY_CHOICES, default='medium', verbose_name='质量等级')
    is_featured = models.BooleanField(default=False, verbose_name='是否推荐')
    is_trending = models.BooleanField(default=False, verbose_name='是否热门')
    is_premium = models.BooleanField(default=False, verbose_name='是否付费内容')
    
    # 时间信息
    published_at = models.DateTimeField(blank=True, null=True, verbose_name='发布时间')
    scheduled_at = models.DateTimeField(blank=True, null=True, verbose_name='定时发布时间')
    
    # SEO和搜索
    slug = models.SlugField(max_length=200, blank=True, null=True, verbose_name='URL标识')
    keywords = models.JSONField(blank=True, null=True, verbose_name='关键词')
    meta_description = models.CharField(max_length=200, blank=True, null=True, verbose_name='SEO描述')
    search_keywords = models.TextField(blank=True, null=True, verbose_name='搜索关键词')
    
    # 扩展信息
    extra_data = models.JSONField(blank=True, null=True, verbose_name='扩展数据')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['published_at']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['is_trending']),
        ]
    
    def save(self, *args, **kwargs):
        if self.content:
            self.word_count = len(self.content)
            self.reading_time = max(1, self.word_count // 200)  # 假设每分钟200字
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class VideoContent(models.Model):
    """视频内容模型"""
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('pending', '待审核'),
        ('published', '已发布'),
        ('archived', '已归档'),
        ('deleted', '已删除'),
    ]
    
    QUALITY_CHOICES = [
        ('low', '一般'),
        ('medium', '良好'),
        ('high', '优质'),
        ('premium', '精品'),
    ]
    
    # 基本信息
    title = models.CharField(max_length=500, verbose_name='标题')
    subtitle = models.CharField(max_length=500, blank=True, null=True, verbose_name='副标题')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    summary = models.CharField(max_length=1000, blank=True, null=True, verbose_name='摘要')
    
    # 作者和来源
    author = models.CharField(max_length=100, blank=True, null=True, verbose_name='作者')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, 
                               on_delete=models.SET_NULL, related_name='created_videos', verbose_name='创建者')
    source = models.CharField(max_length=100, blank=True, null=True, verbose_name='来源')
    source_url = models.URLField(max_length=500, blank=True, null=True, verbose_name='原始链接')
    
    # 视频文件信息
    video_url = models.URLField(max_length=500, verbose_name='视频链接')
    duration = models.PositiveIntegerField(verbose_name='时长(秒)')
    file_size = models.BigIntegerField(blank=True, null=True, verbose_name='文件大小(字节)')
    
    # 媒体文件
    cover_image = models.URLField(max_length=500, blank=True, null=True, verbose_name='封面图片')
    thumbnail_url = models.URLField(max_length=500, blank=True, null=True, verbose_name='缩略图')
    
    # 视频属性
    resolution = models.CharField(max_length=20, blank=True, null=True, verbose_name='分辨率')
    aspect_ratio = models.CharField(max_length=10, blank=True, null=True, verbose_name='宽高比')
    format = models.CharField(max_length=10, default='mp4', verbose_name='视频格式')
    codec = models.CharField(max_length=20, blank=True, null=True, verbose_name='编码格式')
    bitrate = models.PositiveIntegerField(blank=True, null=True, verbose_name='比特率')
    
    # 多清晰度支持
    video_qualities = models.JSONField(blank=True, null=True, verbose_name='多清晰度链接')
    
    # 字幕和音轨
    subtitles = models.JSONField(blank=True, null=True, verbose_name='字幕信息')
    audio_tracks = models.JSONField(blank=True, null=True, verbose_name='音轨信息')
    
    # 章节和时间戳
    chapters = models.JSONField(blank=True, null=True, verbose_name='章节信息')
    timestamps = models.JSONField(blank=True, null=True, verbose_name='时间戳标记')
    
    # 播放设置
    auto_play = models.BooleanField(default=False, verbose_name='自动播放')
    loop = models.BooleanField(default=False, verbose_name='循环播放')
    
    # 分类和标签
    category = models.ForeignKey(ContentCategory, null=True, blank=True, on_delete=models.SET_NULL,
                                related_name='videos', verbose_name='分类')
    tags = models.ManyToManyField(ContentTag, blank=True, verbose_name='标签')
    
    # 状态和质量
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='状态')
    quality_level = models.CharField(max_length=20, choices=QUALITY_CHOICES, default='medium', verbose_name='质量等级')
    is_featured = models.BooleanField(default=False, verbose_name='是否推荐')
    is_trending = models.BooleanField(default=False, verbose_name='是否热门')
    is_premium = models.BooleanField(default=False, verbose_name='是否付费内容')
    
    # 时间信息
    published_at = models.DateTimeField(blank=True, null=True, verbose_name='发布时间')
    scheduled_at = models.DateTimeField(blank=True, null=True, verbose_name='定时发布时间')
    
    # SEO和搜索
    slug = models.SlugField(max_length=200, blank=True, null=True, verbose_name='URL标识')
    keywords = models.JSONField(blank=True, null=True, verbose_name='关键词')
    meta_description = models.CharField(max_length=200, blank=True, null=True, verbose_name='SEO描述')
    search_keywords = models.TextField(blank=True, null=True, verbose_name='搜索关键词')
    
    # 扩展信息
    extra_data = models.JSONField(blank=True, null=True, verbose_name='扩展数据')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '视频'
        verbose_name_plural = '视频'
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['published_at']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['is_trending']),
        ]
    
    def __str__(self):
        return self.title

class AudioContent(models.Model):
    """音频内容模型"""
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('pending', '待审核'),
        ('published', '已发布'),
        ('archived', '已归档'),
        ('deleted', '已删除'),
    ]
    
    QUALITY_CHOICES = [
        ('low', '一般'),
        ('medium', '良好'),
        ('high', '优质'),
        ('premium', '精品'),
    ]
    
    # 基本信息
    title = models.CharField(max_length=500, verbose_name='标题')
    subtitle = models.CharField(max_length=500, blank=True, null=True, verbose_name='副标题')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    summary = models.CharField(max_length=1000, blank=True, null=True, verbose_name='摘要')
    
    # 作者和来源
    author = models.CharField(max_length=100, blank=True, null=True, verbose_name='作者')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, 
                               on_delete=models.SET_NULL, related_name='created_audios', verbose_name='创建者')
    source = models.CharField(max_length=100, blank=True, null=True, verbose_name='来源')
    source_url = models.URLField(max_length=500, blank=True, null=True, verbose_name='原始链接')
    
    # 音频文件信息
    audio_url = models.URLField(max_length=500, verbose_name='音频链接')
    duration = models.PositiveIntegerField(verbose_name='时长(秒)')
    file_size = models.BigIntegerField(blank=True, null=True, verbose_name='文件大小(字节)')
    
    # 媒体文件
    cover_image = models.URLField(max_length=500, blank=True, null=True, verbose_name='封面图片')
    thumbnail_url = models.URLField(max_length=500, blank=True, null=True, verbose_name='缩略图')
    
    # 音频属性
    format = models.CharField(max_length=10, default='mp3', verbose_name='音频格式')
    bitrate = models.PositiveIntegerField(blank=True, null=True, verbose_name='比特率')
    sample_rate = models.PositiveIntegerField(blank=True, null=True, verbose_name='采样率')
    channels = models.PositiveIntegerField(default=2, verbose_name='声道数')
    
    # 多音质支持
    audio_qualities = models.JSONField(blank=True, null=True, verbose_name='多音质链接')
    
    # 音频特有信息
    genre = models.CharField(max_length=50, blank=True, null=True, verbose_name='音频类型')
    artist = models.CharField(max_length=100, blank=True, null=True, verbose_name='艺术家/主播')
    album = models.CharField(max_length=200, blank=True, null=True, verbose_name='专辑/系列')
    
    # 章节和歌词
    chapters = models.JSONField(blank=True, null=True, verbose_name='章节信息')
    lyrics = models.TextField(blank=True, null=True, verbose_name='歌词/文本')
    transcript = models.TextField(blank=True, null=True, verbose_name='转录文本')
    
    # 播放设置
    auto_play = models.BooleanField(default=False, verbose_name='自动播放')
    loop = models.BooleanField(default=False, verbose_name='循环播放')
    
    # 分类和标签
    category = models.ForeignKey(ContentCategory, null=True, blank=True, on_delete=models.SET_NULL,
                                related_name='audios', verbose_name='分类')
    tags = models.ManyToManyField(ContentTag, blank=True, verbose_name='标签')
    
    # 状态和质量
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='状态')
    quality_level = models.CharField(max_length=20, choices=QUALITY_CHOICES, default='medium', verbose_name='质量等级')
    is_featured = models.BooleanField(default=False, verbose_name='是否推荐')
    is_trending = models.BooleanField(default=False, verbose_name='是否热门')
    is_premium = models.BooleanField(default=False, verbose_name='是否付费内容')
    
    # 时间信息
    published_at = models.DateTimeField(blank=True, null=True, verbose_name='发布时间')
    scheduled_at = models.DateTimeField(blank=True, null=True, verbose_name='定时发布时间')
    
    # SEO和搜索
    slug = models.SlugField(max_length=200, blank=True, null=True, verbose_name='URL标识')
    keywords = models.JSONField(blank=True, null=True, verbose_name='关键词')
    meta_description = models.CharField(max_length=200, blank=True, null=True, verbose_name='SEO描述')
    search_keywords = models.TextField(blank=True, null=True, verbose_name='搜索关键词')
    
    # 扩展信息
    extra_data = models.JSONField(blank=True, null=True, verbose_name='扩展数据')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '音频'
        verbose_name_plural = '音频'
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['published_at']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['is_trending']),
        ]
    
    def __str__(self):
        return self.title

class ContentTagRelation(models.Model):
    """内容与标签关联表，支持任意内容类型"""
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='内容类型')
    object_id = models.PositiveIntegerField(verbose_name='内容ID')
    content_object = GenericForeignKey('content_type', 'object_id')
    tag = models.ForeignKey(ContentTag, on_delete=models.CASCADE, verbose_name='标签')
    relevance_score = models.DecimalField(max_digits=5, decimal_places=2, default=1.0, verbose_name='相关度分值')
    confidence_score = models.DecimalField(max_digits=5, decimal_places=2, default=1.0, verbose_name='置信度分值')
    is_auto_tagged = models.BooleanField(default=False, verbose_name='是否自动标记')
    tagged_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, 
                                 on_delete=models.SET_NULL, verbose_name='标记者')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        unique_together = ('content_type', 'object_id', 'tag')
        verbose_name = '内容标签关系'
        verbose_name_plural = '内容标签关系'
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['tag']),
            models.Index(fields=['relevance_score']),
        ]

class ContentModeration(models.Model):
    """内容审核表，支持多次审核历史"""
    STATUS_CHOICES = [
        ('pending', '待审核'),
        ('approved', '通过'),
        ('rejected', '拒绝'),
        ('flagged', '标记'),
        ('reviewing', '审核中'),
        ('appealing', '申诉中'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', '低'),
        ('normal', '普通'),
        ('high', '高'),
        ('urgent', '紧急'),
    ]
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='内容类型')
    object_id = models.PositiveIntegerField(verbose_name='内容ID')
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # 审核状态
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='审核状态')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal', verbose_name='优先级')
    
    # 审核人员
    moderator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, 
                                 on_delete=models.SET_NULL, related_name='moderated_contents', verbose_name='审核员')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, 
                                on_delete=models.SET_NULL, related_name='reviewed_contents', verbose_name='复审员')
    
    # 审核信息
    moderation_reason = models.TextField(blank=True, null=True, verbose_name='审核原因')
    moderation_notes = models.TextField(blank=True, null=True, verbose_name='审核备注')
    violation_types = models.JSONField(blank=True, null=True, verbose_name='违规类型')
    
    # AI审核
    ai_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='AI评分')
    ai_flags = models.JSONField(blank=True, null=True, verbose_name='AI标记')
    ai_confidence = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='AI置信度')
    
    # 用户举报
    user_reports_count = models.PositiveIntegerField(default=0, verbose_name='用户举报次数')
    report_reasons = models.JSONField(blank=True, null=True, verbose_name='举报原因')
    
    # 审核时间
    reviewed_at = models.DateTimeField(blank=True, null=True, verbose_name='审核时间')
    appeal_deadline = models.DateTimeField(blank=True, null=True, verbose_name='申诉截止时间')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = '内容审核'
        verbose_name_plural = '内容审核'
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['content_type', 'object_id']),
        ]

class ContentInteractionStats(models.Model):
    """内容互动统计表，支持自动聚合"""
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='内容类型')
    object_id = models.PositiveIntegerField(verbose_name='内容ID')
    content_object = GenericForeignKey('content_type', 'object_id')
    date = models.DateField(null=True, blank=True, verbose_name='统计日期')  # null表示总计
    
    # 基础统计
    view_count = models.PositiveIntegerField(default=0, verbose_name='浏览次数')
    play_count = models.PositiveIntegerField(default=0, verbose_name='播放次数')
    unique_viewers = models.PositiveIntegerField(default=0, verbose_name='独立观看人数')
    
    # 互动统计
    like_count = models.PositiveIntegerField(default=0, verbose_name='点赞数')
    dislike_count = models.PositiveIntegerField(default=0, verbose_name='不喜欢数')
    comment_count = models.PositiveIntegerField(default=0, verbose_name='评论数')
    share_count = models.PositiveIntegerField(default=0, verbose_name='分享数')
    favorite_count = models.PositiveIntegerField(default=0, verbose_name='收藏数')
    download_count = models.PositiveIntegerField(default=0, verbose_name='下载数')
    
    # 质量评价
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True, verbose_name='平均评分')
    rating_count = models.PositiveIntegerField(default=0, verbose_name='评分人数')
    
    # 播放统计（针对音视频内容）
    total_play_time = models.BigIntegerField(default=0, verbose_name='总播放时长(秒)')
    avg_play_time = models.PositiveIntegerField(default=0, verbose_name='平均播放时长(秒)')
    completion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='完播率')
    
    # 阅读统计（针对文章内容）
    total_reading_time = models.BigIntegerField(default=0, verbose_name='总阅读时长(秒)')
    avg_reading_time = models.PositiveIntegerField(default=0, verbose_name='平均阅读时长(秒)')
    reading_progress = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='平均阅读进度')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        unique_together = ('content_type', 'object_id', 'date')
        verbose_name = '内容统计'
        verbose_name_plural = '内容统计'
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['date']),
            models.Index(fields=['play_count']),
            models.Index(fields=['like_count']),
        ]

class UserContentInteraction(models.Model):
    """用户内容交互记录"""
    INTERACTION_TYPES = [
        ('view', '浏览'),
        ('play', '播放'),
        ('like', '点赞'),
        ('dislike', '不喜欢'),
        ('favorite', '收藏'),
        ('share', '分享'),
        ('comment', '评论'),
        ('download', '下载'),
        ('rating', '评分'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='用户')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='内容类型')
    object_id = models.PositiveIntegerField(verbose_name='内容ID')
    content_object = GenericForeignKey('content_type', 'object_id')
    
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES, verbose_name='交互类型')
    value = models.DecimalField(max_digits=10, decimal_places=2, default=1, verbose_name='交互值')
    
    # 详细信息
    metadata = models.JSONField(blank=True, null=True, verbose_name='交互元数据')
    device_info = models.JSONField(blank=True, null=True, verbose_name='设备信息')
    
    # 时间和位置
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='交互时间')
    session_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='会话ID')
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name='IP地址')
    
    class Meta:
        verbose_name = '用户交互'
        verbose_name_plural = '用户交互'
        indexes = [
            models.Index(fields=['user', 'interaction_type']),
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['created_at']),
        ]

# 兼容现有的RawNews模型，但扩展其功能
class RawNews(models.Model):
    """原始新闻内容表 - 增强版本"""
    TYPE_CHOICES = [
        ('audio', '音频'),
        ('video', '视频'),
        ('article', '文章'),
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='article', verbose_name='内容类型')
    source = models.CharField(max_length=100, blank=True, null=True, verbose_name='来源')
    title = models.CharField(max_length=500, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    summary = models.TextField(blank=True, null=True, verbose_name='摘要')
    author = models.CharField(max_length=100, blank=True, null=True, verbose_name='作者')
    source_url = models.URLField(max_length=500, unique=True, verbose_name='原始链接')
    image_urls = models.JSONField(blank=True, null=True, verbose_name='图片链接')
    published_at = models.DateTimeField(verbose_name='发布时间')
    crawled_at = models.DateTimeField(auto_now_add=True, verbose_name='抓取时间')
    language = models.CharField(max_length=10, default='zh-CN', verbose_name='语言')
    
    # 分类和标签
    category = models.ForeignKey(ContentCategory, null=True, blank=True, on_delete=models.SET_NULL,
                                verbose_name='分类')
    tags = models.JSONField(blank=True, null=True, verbose_name='标签')
    keywords = models.JSONField(blank=True, null=True, verbose_name='关键词')
    
    # AI分析结果
    sentiment_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='情感分值')
    importance_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='重要性分值')
    relevance_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='相关性分值')
    quality_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='质量分值')
    
    # 处理状态
    is_processed = models.BooleanField(default=False, verbose_name='是否已处理')
    is_duplicate = models.BooleanField(default=False, verbose_name='是否重复')
    
    # 生成的内容关联
    generated_article = models.OneToOneField('Article', null=True, blank=True, on_delete=models.SET_NULL,
                                           verbose_name='生成的文章')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '原始新闻'
        verbose_name_plural = '原始新闻'
        ordering = ['-published_at', '-crawled_at']
    
    def __str__(self):
        return self.title 