from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Quiz, Question, Choice, QuizAttempt, QuestionResponse
from .serializers import (
    QuizSerializer, QuestionSerializer, ChoiceSerializer,
    QuizAttemptSerializer, QuestionResponseSerializer
)
from .permissions import IsTutorOrGuideOrReadOnly
from django.utils import timezone

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsTutorOrGuideOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def start(self, request, pk=None):
        quiz = self.get_object()
        attempt = QuizAttempt.objects.create(quiz=quiz, user=request.user)
        return Response({"attempt_id": attempt.id}, status=201)

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsTutorOrGuideOrReadOnly]

class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [IsTutorOrGuideOrReadOnly]

class QuizAttemptViewSet(viewsets.ModelViewSet):
    queryset = QuizAttempt.objects.all()
    serializer_class = QuizAttemptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self.request.user, "role", None) in ("tutor", "guide"):
            return QuizAttempt.objects.all()
        return QuizAttempt.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def submit(self, request, pk=None):
        attempt = self.get_object()
        if attempt.user != request.user:
            return Response({"detail": "Not your attempt."}, status=403)
        data = request.data.get('responses', [])
        total = 0
        correct = 0
        for item in data:
            qid = item.get('question')
            resp, _ = QuestionResponse.objects.get_or_create(attempt=attempt, question_id=qid)
            question = resp.question
            if question.type in ['mcq', 'multi']:
                resp.selected_choices.clear()
                selected = item.get('selected_choices', [])
                for cid in selected:
                    resp.selected_choices.add(cid)
                # Scoring
                if question.type == 'mcq':
                    correct_choice = question.choices.filter(is_correct=True).first()
                    if correct_choice and len(selected) == 1 and int(selected[0]) == correct_choice.id:
                        correct += 1
                elif question.type == 'multi':
                    correct_choices = set(question.choices.filter(is_correct=True).values_list('id', flat=True))
                    if set(map(int, selected)) == correct_choices:
                        correct += 1
            elif question.type == 'open':
                resp.text_answer = item.get('text_answer', '')
                # Tutor/guide should review open-ended
            resp.save()
            total += 1
        # Calculate score (only for auto-gradable questions)
        if total > 0:
            attempt.score = round((correct / total) * 100, 2)
        attempt.completed_at = timezone.now()
        attempt.save()
        return Response({"score": attempt.score}, status=200)

    @action(detail=True, methods=['post'], permission_classes=[IsTutorOrGuideOrReadOnly])
    def feedback(self, request, pk=None):
        attempt = self.get_object()
        feedback = request.data.get('feedback', '')
        attempt.feedback = feedback
        attempt.save()
        return Response({"status": "Feedback added"})

class QuestionResponseViewSet(viewsets.ModelViewSet):
    queryset = QuestionResponse.objects.all()
    serializer_class = QuestionResponseSerializer
    permission_classes = [permissions.IsAuthenticated]