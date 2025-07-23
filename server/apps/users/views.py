from django.shortcuts import render
from rest_framework import generics, permissions
from .models import User
from .serializers import UserSerializer

# Create your views here.

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self):
        return self.request.user
