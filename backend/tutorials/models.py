from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Tutorial(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tutorials',
        verbose_name=_("Author")
    )
    category = models.ForeignKey(
        'TutorialCategory',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tutorials',
        verbose_name=_("Category")
    )
    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_("Description"))
    video_url = models.URLField(_("Video URL"), blank=True, null=True)
    language = models.CharField(_("Language"), max_length=50, blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)  # 💰
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Tutorial")
        verbose_name_plural = _("Tutorials")

    def __str__(self):
        return self.title


class TutorialStep(models.Model):
    tutorial = models.ForeignKey(
        Tutorial,
        on_delete=models.CASCADE,
        related_name='steps',
        verbose_name=_("Tutorial")
    )
    title = models.CharField(_("Title"), max_length=255)
    content = models.TextField(_("Content"))
    step_number = models.PositiveIntegerField(_("Step Number"))

    class Meta:
        ordering = ['step_number']
        verbose_name = _("Tutorial Step")
        verbose_name_plural = _("Tutorial Steps")

    def __str__(self):
        return f"{self.tutorial.title} - {_('Step')} {self.step_number}"


class TutorialCategory(models.Model):
    name = models.CharField(_("Name"), max_length=100, unique=True)
    description = models.TextField(_("Description"), blank=True, null=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = _("Tutorial Category")
        verbose_name_plural = _("Tutorial Categories")

    def __str__(self):
        return self.name

    def get_tutorial_count(self):
        """Returns the number of tutorials associated with this category."""
        return self.tutorials.count()

class TutorialEnrollment(models.Model):
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE, related_name='enrollments')
    learner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('tutorial', 'learner')
        verbose_name = _("Tutorial Enrollment")
        verbose_name_plural = _("Tutorial Enrollments")
        
