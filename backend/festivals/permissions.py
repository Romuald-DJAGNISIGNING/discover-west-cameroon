from rest_framework import permissions

class IsTutorOrGuideOrReadOnly(permissions.BasePermission):
    """
    Tutors and guides can create/update/delete; others read-only.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        return getattr(user, 'role', None) in ('tutor', 'guide')

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        if hasattr(obj, 'added_by'):
            return obj.added_by == user or getattr(user, 'role', None) in ('tutor', 'guide')
        return getattr(user, 'role', None) in ('tutor', 'guide')

class IsAttendanceOwnerOrReadOnly(permissions.BasePermission):
    """
    Only the owner of the attendance can modify feedback/attendance.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class IsAttendeeOrReadOnly(permissions.BasePermission):
    """
    Only festival attendees can post feedback/experiences.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if hasattr(view, 'get_object'):
            obj = view.get_object()
            if hasattr(obj, 'user'):
                return obj.user == request.user
            if hasattr(obj, 'attendance') and hasattr(obj.attendance, 'user'):
                return obj.attendance.user == request.user
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if hasattr(obj, 'user'):
            return obj.user == request.user
        if hasattr(obj, 'attendance') and hasattr(obj.attendance, 'user'):
            return obj.attendance.user == request.user
        return False