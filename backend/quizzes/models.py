from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Quiz(models.Model):
    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_("Description"), blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='quizzes',
        verbose_name=_("Created By")
    )
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Quiz")
        verbose_name_plural = _("Quizzes")
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name=_("Quiz")
    )
    text = models.TextField(_("Question Text"))

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")

    def __str__(self):
        return f"{_('Question for')} {self.quiz.title}"


class QuizSubmission(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='quiz_submissions',
        verbose_name=_("User")
    )
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='submissions',
        verbose_name=_("Quiz")
    )
    score = models.FloatField(_("Score"))
    submitted_at = models.DateTimeField(_("Submitted At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Quiz Submission")
        verbose_name_plural = _("Quiz Submissions")
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.user.email} - {self.quiz.title} - {self.score}"


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name=_("Question")
    )
    text = models.CharField(_("Choice Text"), max_length=255)
    is_correct = models.BooleanField(_("Is Correct"), default=False)

    class Meta:
        verbose_name = _("Choice")
        verbose_name_plural = _("Choices")

    def __str__(self):
        return self.text


class UserQuizProgress(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("User")
    )
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        verbose_name=_("Quiz")
    )
    progress = models.IntegerField(_("Progress"), default=0)
    score = models.FloatField(_("Score"), default=0.0)
    completed = models.BooleanField(_("Completed"), default=False)

    class Meta:
        verbose_name = _("User Quiz Progress")
        verbose_name_plural = _("User Quiz Progresses")

    def __str__(self):
        return f"{self.user.email} - {self.quiz.title} - {self.progress}%"