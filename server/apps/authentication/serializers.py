from rest_framework import serializers
from apps.users.models import User
from django.contrib.auth.hashers import make_password

class RegisterSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'nickname', 'phone']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("两次密码不一致")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        validated_data['password_hash'] = make_password(validated_data.pop('password'))
        return super().create(validated_data)

class LoginSerializer(serializers.Serializer):
    """用户登录序列化器"""
    login = serializers.CharField()  # 用户名或邮箱
    password = serializers.CharField(write_only=True)
    # 可扩展 device_info 字段

class UserProfileSerializer(serializers.ModelSerializer):
    """用户信息序列化器"""
    class Meta:
        model = User
        exclude = ['password_hash']

class AvatarUploadSerializer(serializers.Serializer):
    """头像上传序列化器"""
    avatar = serializers.ImageField() 