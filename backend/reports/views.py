from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Report
from .serializers import ReportSerializer
from .permissions import IsAdminReviewerOrOwnerOrReadOnly


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all().order_by('-created_at')
    serializer_class = ReportSerializer
    permission_classes = [IsAdminReviewerOrOwnerOrReadOnly]
    filterset_fields = ['type', 'status', 'village', 'attraction', 'festival']

    def perform_create(self, serializer):
        serializer.save(reported_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminReviewerOrOwnerOrReadOnly])
    def review(self, request, pk=None):
        report = self.get_object()
        report.status = 'reviewed'
        report.reviewed_by = request.user
        report.resolution_comment = request.data.get("resolution_comment", "")
        report.save()
        return Response({"status": "reviewed", "id": report.id})

    @action(detail=True, methods=['post'], permission_classes=[IsAdminReviewerOrOwnerOrReadOnly])
    def resolve(self, request, pk=None):
        report = self.get_object()
        report.status = 'resolved'
        report.reviewed_by = request.user
        report.resolution_comment = request.data.get("resolution_comment", "")
        report.save()
        return Response({"status": "resolved", "id": report.id})

    @action(detail=True, methods=['post'], permission_classes=[IsAdminReviewerOrOwnerOrReadOnly])
    def close(self, request, pk=None):
        report = self.get_object()
        report.status = 'closed'
        report.reviewed_by = request.user
        report.resolution_comment = request.data.get("resolution_comment", "")
        report.save()
        return Response({"status": "closed", "id": report.id})
        
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['is_owner'] = False
        
        # Only check ownership if this is a detail view (has pk)
        if (self.request.user.is_authenticated and 
            hasattr(self, 'kwargs') and 
            'pk' in self.kwargs):
            try:
                obj = self.get_object()
                context['is_owner'] = (obj.reported_by == self.request.user)
            except (AssertionError, Report.DoesNotExist):
                pass
                
        return context