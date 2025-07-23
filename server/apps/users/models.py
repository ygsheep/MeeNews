from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """自定义用户模型，兼容Django认证体系，可扩展"""
    nickname = models.CharField(max_length=50, blank=True, null=True, verbose_name='昵称')
    avatar_url = models.URLField(max_length=255, blank=True, null=True, verbose_name='头像')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='手机号')
    bio = models.TextField(blank=True, null=True, verbose_name='个人简介')
    is_verified = models.BooleanField(default=False, verbose_name='是否已认证')
    premium_until = models.DateTimeField(blank=True, null=True, verbose_name='会员到期时间')
    interest_tags = models.JSONField(blank=True, null=True, verbose_name='兴趣标签')
    listening_preferences = models.JSONField(blank=True, null=True, verbose_name='听音偏好')
    location = models.CharField(max_length=100, blank=True, null=True, verbose_name='位置信息')
    last_login_at = models.DateTimeField(blank=True, null=True, verbose_name='最后登录时间')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.username
