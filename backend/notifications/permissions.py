from rest_framework import permissions

class IsNotificationRecipientOrReadOnly(permissions.BasePermission):
    """
    Only the recipient can mark as read/delete, others read-only.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.recipient == request.user
        return obj.recipient == request.user