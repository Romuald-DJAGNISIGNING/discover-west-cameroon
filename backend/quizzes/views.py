

from rest_framework import generics, permissions
from .models import Quiz, QuizSubmission
from .serializers import (
    QuizSerializer, QuizCreateSerializer,
    QuizSubmissionSerializer
)
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

class QuizListCreateView(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return QuizCreateSerializer
        return QuizSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class QuizDetailView(generics.RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.AllowAny]


class SubmitQuizView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        user_answers = request.data.get("answers", {})

        total_questions = quiz.questions.count()
        correct_answers = 0

        for question in quiz.questions.all():
            selected_choice_id = user_answers.get(str(question.id))
            if question.choices.filter(id=selected_choice_id, is_correct=True).exists():
                correct_answers += 1

        score = (correct_answers / total_questions) * 100 if total_questions else 0

        submission = QuizSubmission.objects.create(
            user=request.user,
            quiz=quiz,
            score=score
        )
        serializer = QuizSubmissionSerializer(submission)
        return Response(serializer.data)
