from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Tutorial, TutorialStep
from .serializers import TutorialSerializer, TutorialStepSerializer
from rest_framework.exceptions import PermissionDenied

class TutorialViewSet(viewsets.ModelViewSet):
    queryset = Tutorial.objects.all().order_by('-created_at')
    serializer_class = TutorialSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("You are not allowed to edit this tutorial.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("You are not allowed to delete this tutorial.")
        instance.delete()


class TutorialStepViewSet(viewsets.ModelViewSet):
    queryset = TutorialStep.objects.all().order_by('step_number')
    serializer_class = TutorialStepSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        tutorial = serializer.validated_data.get('tutorial')
        if tutorial.author != self.request.user:
            raise PermissionDenied("You can only add steps to your own tutorials.")
        serializer.save()

    def perform_update(self, serializer):
        if serializer.instance.tutorial.author != self.request.user:
            raise PermissionDenied("You can only edit steps of your own tutorials.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.tutorial.author != self.request.user:
            raise PermissionDenied("You can only delete steps from your own tutorials.")
        instance.delete()
