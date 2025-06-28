from rest_framework import permissions

class IsTutorOrGuide(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return getattr(user, "role", None) in ("tutor", "guide", "admin") or user.is_superuser

class IsOwnerOrSuperuser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'created_by'):  # For Tutorial model
            return obj.created_by == request.user or request.user.is_superuser
        elif hasattr(obj, 'user'):  # For TutorialComment model
            return obj.user == request.user or request.user.is_superuser
        return False

class IsOwnerAndTutorOrGuide(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return getattr(user, "role", None) in ("tutor", "guide", "admin") or user.is_superuser

    def has_object_permission(self, request, view, obj):
        is_owner = obj.created_by == request.user
        has_role = getattr(request.user, "role", None) in ("tutor", "guide", "admin")
        return is_owner and has_role

class IsTutorOrGuideOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        return getattr(user, "role", None) in ("tutor", "guide", "admin") or user.is_superuser

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        is_owner = obj.created_by == request.user
        has_role = getattr(request.user, "role", None) in ("tutor", "guide", "admin")
        return (is_owner and has_role) or request.user.is_superuser