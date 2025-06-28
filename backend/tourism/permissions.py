from rest_framework import permissions

class IsGuideOrTutorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        return getattr(user, 'role', None) in ('tutor', 'guide')

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        return getattr(user, 'role', None) in ('tutor', 'guide') or obj.added_by == user