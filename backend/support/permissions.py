from rest_framework import permissions

class IsTicketOwnerOrStaffOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.method == "POST":
            return True
        user = request.user
        # Ticket owner, assigned staff, admin or superuser can edit/update
        return obj.created_by == user or user == obj.assigned_to or user.is_superuser or getattr(user, "role", None) in ("admin", "tutor", "guide")