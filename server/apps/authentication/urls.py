from django.urls import path
from .views import RegisterView, LoginView, CustomTokenRefreshView, UserProfileView, AvatarUploadView

urlpatterns = [
    path('auth/register', RegisterView.as_view()),  # 用户注册
    path('auth/login', LoginView.as_view()),        # 用户登录
    path('auth/refresh', CustomTokenRefreshView.as_view()),  # Token刷新
    path('users/profile', UserProfileView.as_view()),        # 用户信息
    path('users/avatar', AvatarUploadView.as_view()),        # 头像上传
] 