from rest_framework import permissions

class IsAdminReviewerOrOwnerOrReadOnly(permissions.BasePermission):
    """
    - Anyone can create and read reports
    - Only admins/reviewers can update the status and resolution
    - Only the report owner can update their own report (not status!)
    """
    def has_permission(self, request, view):
        # Allow all for safe methods or POST
        if request.method in permissions.SAFE_METHODS or request.method == "POST":
            return True
        
        # For other methods, we'll check object permissions
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
            
        user = request.user
        
        # Allow admins/reviewers full access
        if user.is_superuser or getattr(user, "role", None) in ("admin", "tutor", "guide"):
            return True
            
        # Allow owner to update their report (except status/resolution)
        if obj.reported_by == user and request.method in ["PUT", "PATCH"]:
            # Check if trying to modify restricted fields
            restricted_fields = {'status', 'resolution_comment', 'reviewed_by'}
            if not any(field in request.data for field in restricted_fields):
                return True
                
        return False