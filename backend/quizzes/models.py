from django.db import models
from django.conf import settings
from villages.models import Village
from tourism.models import TouristicAttraction

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    village = models.ForeignKey(Village, related_name="quizzes", null=True, blank=True, on_delete=models.SET_NULL)
    attraction = models.ForeignKey(TouristicAttraction, related_name="quizzes", null=True, blank=True, on_delete=models.SET_NULL)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class Question(models.Model):
    QUESTION_TYPES = (
        ('mcq', 'Multiple Choice (Single)'),
        ('multi', 'Multiple Choice (Multiple)'),
        ('open', 'Open Ended'),
    )
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    type = models.CharField(max_length=8, choices=QUESTION_TYPES)
    order = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quiz.title}: {self.text[:40]}"

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class QuizAttempt(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='attempts', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='quiz_attempts', on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.FloatField(default=0)
    feedback = models.TextField(blank=True)  # Tutor/guide can add feedback

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}"

class QuestionResponse(models.Model):
    attempt = models.ForeignKey(QuizAttempt, related_name='responses', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choices = models.ManyToManyField(Choice, blank=True)
    text_answer = models.TextField(blank=True)

    def __str__(self):
        return f"Attempt {self.attempt.id} - Q: {self.question.id}"