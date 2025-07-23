from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'nickname', 'avatar_url', 'phone', 'bio', 'is_verified', 'premium_until', 'interest_tags', 'listening_preferences', 'location', 'last_login_at', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at'] 