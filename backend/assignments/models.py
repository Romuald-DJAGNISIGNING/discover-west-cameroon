from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Assignment(models.Model):
    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_("Description"))
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    due_date = models.DateTimeField(_("Due Date"))
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='assigned_assignments',
        on_delete=models.CASCADE,
        verbose_name=_("Assigned By")
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='received_assignments',
        on_delete=models.CASCADE,
        verbose_name=_("Assigned To")
    )

    class Meta:
        verbose_name = _("Assignment")
        verbose_name_plural = _("Assignments")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.assigned_to.username}"

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
        verbose_name=_("Student")
    )
    submitted_at = models.DateTimeField(_("Submitted At"), auto_now_add=True)
    file = models.FileField(_("File"), upload_to='assignment_submissions/')
    grade = models.DecimalField(_("Grade"), max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(_("Feedback"), null=True, blank=True)

    class Meta:
        verbose_name = _("Assignment Submission")
        verbose_name_plural = _("Assignment Submissions")
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{_('Submission by')} {self.student.username} {_('for')} {self.assignment.title}"
