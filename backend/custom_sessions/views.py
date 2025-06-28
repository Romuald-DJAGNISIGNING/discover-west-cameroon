from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import CustomSession, SessionMaterial, SessionFeedback, InAppNotification
from .serializers import (
    CustomSessionSerializer,
    SessionMaterialSerializer,
    SessionFeedbackSerializer,
    InAppNotificationSerializer,
)
from rest_framework.decorators import action

class IsLearner(permissions.BasePermission):
    def has_permission(self, request, view):
        return getattr(request.user, 'role', None) == 'learner'

class IsVisitor(permissions.BasePermission):
    def has_permission(self, request, view):
        return getattr(request.user, 'role', None) == 'visitor'

class CustomSessionViewSet(viewsets.ModelViewSet):
    queryset = CustomSession.objects.all()
    serializer_class = CustomSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        session = self.get_object()
        if request.user not in [session.tutor_or_guide, session.learner_or_visitor]:
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
        session.mark_confirmed()
        return Response({"status": "confirmed"})

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        session = self.get_object()
        if request.user != session.tutor_or_guide:
            return Response({"detail": "Only the tutor/guide can complete sessions"}, status=status.HTTP_403_FORBIDDEN)
        session.mark_completed()
        return Response({"status": "completed"})

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        session = self.get_object()
        if request.user not in [session.tutor_or_guide, session.learner_or_visitor]:
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
        reason = request.data.get("reason", "")
        session.mark_cancelled(reason=reason)
        return Response({"status": "cancelled", "reason": reason})

    @action(detail=True, methods=['post'])
    def no_show(self, request, pk=None):
        session = self.get_object()
        if request.user != session.tutor_or_guide:
            return Response({"detail": "Only the tutor/guide can mark as no-show"}, status=status.HTTP_403_FORBIDDEN)
        session.mark_no_show()
        return Response({"status": "no_show"})

class SessionMaterialViewSet(viewsets.ModelViewSet):
    queryset = SessionMaterial.objects.all()
    serializer_class = SessionMaterialSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

class SessionFeedbackViewSet(viewsets.ModelViewSet):
    queryset = SessionFeedback.objects.all()
    serializer_class = SessionFeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class InAppNotificationViewSet(viewsets.ModelViewSet):
    serializer_class = InAppNotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'patch', 'head', 'options']

    def get_queryset(self):
        return InAppNotification.objects.filter(user=self.request.user)