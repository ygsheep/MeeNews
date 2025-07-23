from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer, AvatarUploadSerializer
from apps.users.models import User
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.parsers import MultiPartParser, FormParser

class RegisterView(APIView):
    """用户注册API"""
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "success": True,
                "data": {
                    "user": UserProfileSerializer(user).data,
                    "token": {
                        "access": str(refresh.access_token),
                        "refresh": str(refresh),
                        "expires_in": 3600
                    }
                }
            }, status=status.HTTP_201_CREATED)
        return Response({"success": False, "errors": serializer.errors}, status=400)

class LoginView(APIView):
    """用户登录API"""
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            login = serializer.validated_data['login']
            password = serializer.validated_data['password']
            user = User.objects.filter(username=login).first() or User.objects.filter(email=login).first()
            if user and check_password(password, user.password_hash):
                refresh = RefreshToken.for_user(user)
                return Response({
                    "success": True,
                    "data": {
                        "user": UserProfileSerializer(user).data,
                        "token": {
                            "access": str(refresh.access_token),
                            "refresh": str(refresh),
                            "expires_in": 3600
                        }
                    }
                })
            return Response({"success": False, "message": "用户名或密码错误"}, status=400)
        return Response({"success": False, "errors": serializer.errors}, status=400)

class CustomTokenRefreshView(TokenRefreshView):
    """Token刷新API，返回自定义响应格式"""
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            return Response({
                "success": True,
                "data": {
                    "token": {
                        "access": response.data.get('access'),
                        "refresh": request.data.get('refresh'),
                        "expires_in": 3600
                    }
                }
            })
        return Response({"success": False, "errors": response.data}, status=response.status_code)

class UserProfileView(APIView):
    """获取和更新用户信息API"""
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response({"success": True, "data": serializer.data})
    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data})
        return Response({"success": False, "errors": serializer.errors}, status=400)

class AvatarUploadView(APIView):
    """头像上传API"""
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request):
        serializer = AvatarUploadSerializer(data=request.data)
        if serializer.is_valid():
            avatar = serializer.validated_data['avatar']
            user = request.user
            # 假设User模型有avatar_url字段
            user.avatar_url = avatar
            user.save()
            return Response({"success": True, "data": {"avatar_url": user.avatar_url}})
        return Response({"success": False, "errors": serializer.errors}, status=400)
