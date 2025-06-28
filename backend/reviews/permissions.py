from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions allowed to any request,
        # Write permissions only to the owner of the review.
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user