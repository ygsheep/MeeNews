from django.urls import path
from .views import UserProfileView

urlpatterns = [
    path('users/profile', UserProfileView.as_view()),
] 