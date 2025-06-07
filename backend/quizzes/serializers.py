

from rest_framework import serializers
from .models import Quiz, Question, Choice, QuizSubmission

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'choices']


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    created_by = serializers.StringRelatedField()

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'created_by', 'created_at', 'questions']


class QuizCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description']


class QuizSubmissionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    quiz = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = QuizSubmission
        fields = ['id', 'user', 'quiz', 'score', 'submitted_at']
