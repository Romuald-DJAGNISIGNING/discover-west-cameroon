from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Tutorial, TutorialStep, TutorialEnrollment
from .serializers import TutorialSerializer, TutorialStepSerializer
from rest_framework.exceptions import PermissionDenied
from payments.utils import create_payment_for_tutorial
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from notifications.tasks import notify_user

class EnrollInTutorialView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, tutorial_id):
        tutorial = Tutorial.objects.get(id=tutorial_id)
        user = request.user

        # Check if already enrolled
        if TutorialEnrollment.objects.filter(tutorial=tutorial, learner=user).exists():
            return Response({"message": "Already enrolled."}, status=status.HTTP_200_OK)

        if tutorial.is_free():
            TutorialEnrollment.objects.create(tutorial=tutorial, learner=user, paid=False)

            notify_user.delay(
                user_id=user.id,
                subject="Tutorial Enrolled",
                message=f"You've successfully enrolled in {tutorial.title}.",
                in_app_title="Enrollment Successful",
                in_app_type="success",
                link=f"/dashboard/learner/tutorials/"
            )
            return Response({"message": "Enrolled in free tutorial."}, status=status.HTTP_201_CREATED)
        else:
            # 👇 Paid tutorial - Create payment object and wait for confirmation
            payment = create_payment_for_tutorial(user, tutorial)
            return Response({
                "message": "Payment required.",
                "payment_id": payment.id,
                "amount": str(payment.amount),
                "tutorial_id": tutorial.id
            }, status=status.HTTP_202_ACCEPTED)




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
