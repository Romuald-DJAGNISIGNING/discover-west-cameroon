
from rest_framework import generics, permissions, filters
from .models import Festival
from .serializers import FestivalSerializer

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission: allow read-only for all, write only for admin.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class FestivalListCreateView(generics.ListCreateAPIView):
    queryset = Festival.objects.all().order_by('-start_date')
    serializer_class = FestivalSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'location', 'description']
    ordering_fields = ['start_date', 'end_date']

class FestivalDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Festival.objects.all()
    serializer_class = FestivalSerializer
    permission_classes = [IsAdminOrReadOnly]
