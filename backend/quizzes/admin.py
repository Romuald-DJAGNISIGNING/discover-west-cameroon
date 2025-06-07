from django.contrib import admin
from .models import Quiz, Question, Choice, UserQuizProgress

class AnswerInline(admin.TabularInline):
    model = Choice
    extra = 2

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ('text', 'quiz')

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')

@admin.register(UserQuizProgress)
class UserQuizProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'completed')

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'is_correct')
    list_filter = ('is_correct', 'question')
    search_fields = ('text',)
