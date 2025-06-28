from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone

class Assignment(models.Model):
    class AssignmentType(models.TextChoices):
        TUTORING = "tutoring", _("Tutoring")
        TOUR = "tour", _("Tour Guide")

    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_("Description"))
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    due_date = models.DateTimeField(_("Due Date"))
    assignment_type = models.CharField(
        _("Assignment Type"),
        max_length=16,
        choices=AssignmentType.choices,
        default=AssignmentType.TUTORING,
    )
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='assignments_given',
        on_delete=models.CASCADE,
        verbose_name=_("Assigned By"),
        help_text=_("The tutor or guide who creates this assignment."),
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='assignments_received',
        on_delete=models.CASCADE,
        verbose_name=_("Assigned To"),
        help_text=_("The learner who receives this assignment."),
    )
    attachment = models.FileField(_("Attachment (optional)"), upload_to='assignments/attachments/', blank=True, null=True)
    external_link = models.URLField(_("External Link (optional)"), blank=True, null=True)
    is_active = models.BooleanField(_("Is Active"), default=True)

    class Meta:
        verbose_name = _("Assignment")
        verbose_name_plural = _("Assignments")
        ordering = ['-created_at']

    def clean(self):
        if self.assignment_type == self.AssignmentType.TUTORING:
            if getattr(self.assigned_by, 'role', None) != 'tutor':
                raise ValidationError(_("Assigned by must be a tutor for tutoring assignments."))
        elif self.assignment_type == self.AssignmentType.TOUR:
            if getattr(self.assigned_by, 'role', None) != 'guide':
                raise ValidationError(_("Assigned by must be a guide for tour assignments."))
        if getattr(self.assigned_to, 'role', None) != 'learner':
            raise ValidationError(_("Only a learner can be assigned an assignment."))
        if self.due_date < timezone.now():
            raise ValidationError(_("Due date cannot be in the past."))

    def __str__(self):
        return f"{self.title} [{self.assignment_type}] -> {self.assigned_to.username}"

class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(
        Assignment,
        related_name='submissions',
        on_delete=models.CASCADE,
        verbose_name=_("Assignment")
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("Learner"),
        help_text=_("The learner submitting.")
    )
    submitted_at = models.DateTimeField(_("Submitted At"), auto_now_add=True)
    file = models.FileField(_("File"), upload_to='assignment_submissions/')
    comment = models.TextField(_("Submission Comment"), blank=True, null=True)
    grade = models.DecimalField(_("Grade"), max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(_("Feedback"), null=True, blank=True)
    is_active = models.BooleanField(_("Is Active"), default=True)

    class Meta:
        verbose_name = _("Assignment Submission")
        verbose_name_plural = _("Assignment Submissions")
        ordering = ['-submitted_at']
        unique_together = ('assignment', 'student')

    def clean(self):
        if getattr(self.student, 'role', None) != 'learner':
            raise ValidationError(_("Only a learner can submit an assignment."))

    def __str__(self):
        return f"{_('Submission by')} {self.student.username} {_('for')} {self.assignment.title}"