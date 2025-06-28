from rest_framework import serializers
from .models import Quiz, Question, Choice, QuizAttempt, QuestionResponse

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text']

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'quiz', 'type', 'text', 'order', 'choices']

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'village', 'attraction', 'created_by', 'created_at', 'questions']

class QuestionResponseSerializer(serializers.ModelSerializer):
    selected_choices = ChoiceSerializer(many=True, read_only=True)
    class Meta:
        model = QuestionResponse
        fields = ['id', 'question', 'selected_choices', 'text_answer']

class QuizAttemptSerializer(serializers.ModelSerializer):
    responses = QuestionResponseSerializer(many=True, read_only=True)
    quiz = QuizSerializer(read_only=True)
    user = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = QuizAttempt
        fields = ['id', 'quiz', 'user', 'started_at', 'completed_at', 'score', 'feedback', 'responses']