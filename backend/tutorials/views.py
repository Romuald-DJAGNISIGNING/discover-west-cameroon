from rest_framework import viewsets, permissions
from django.shortcuts import get_object_or_404
from .models import Tutorial, TutorialCategory, TutorialComment
from .serializers import TutorialSerializer, TutorialCategorySerializer, TutorialCommentSerializer
from .permissions import IsTutorOrGuide, IsOwnerOrSuperuser, IsOwnerAndTutorOrGuide

class TutorialCategoryViewSet(viewsets.ModelViewSet):
    queryset = TutorialCategory.objects.all()
    serializer_class = TutorialCategorySerializer
    permission_classes = [IsTutorOrGuide]

class TutorialViewSet(viewsets.ModelViewSet):
    serializer_class = TutorialSerializer
    filterset_fields = ['is_published', 'category', 'village', 'attraction', 'festival']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsTutorOrGuide & (IsOwnerAndTutorOrGuide | permissions.IsAdminUser)]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Tutorial.objects.all()
        return Tutorial.objects.filter(is_published=True)

class TutorialCommentViewSet(viewsets.ModelViewSet):
    serializer_class = TutorialCommentSerializer
    permission_classes = [permissions.IsAuthenticated & IsOwnerOrSuperuser]

    def get_queryset(self):
        return TutorialComment.objects.all()

    def perform_create(self, serializer):
        # For the custom add-comment endpoint
        if 'tutorial_id' in self.kwargs:
            tutorial = get_object_or_404(Tutorial, id=self.kwargs['tutorial_id'])
            serializer.save(user=self.request.user, tutorial=tutorial)
        else:
            serializer.save(user=self.request.user)