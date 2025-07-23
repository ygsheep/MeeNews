from rest_framework import permissions

class IsAuthorOrAdmin(permissions.BasePermission):
    """仅内容作者或管理员可操作"""
    def has_object_permission(self, request, view, obj):
        return request.user and (request.user.is_staff or getattr(obj, 'author', None) == request.user)

class IsAdminOrReadOnly(permissions.BasePermission):
    """仅管理员可写，其他用户只读"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff 