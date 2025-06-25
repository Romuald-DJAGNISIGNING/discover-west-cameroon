from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


User = get_user_model()

REVIEW_TARGET_CHOICES = [
    ('guide', _("Touristic Guide")),
    ('tutor', _("Tutor")),
    ('site', _("Tourist Site")),
    ('festival', _("Festival")),
    ('village', _("Village")),
]

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    target_type = models.CharField(_("Target Type"), max_length=50, choices=REVIEW_TARGET_CHOICES)
    target_id = models.PositiveIntegerField(_("Target ID"))
    rating = models.PositiveIntegerField(_("Rating"), default=5)
    comment = models.TextField(_("Comment"), blank=True, null=True)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='replies',
        on_delete=models.CASCADE,
        verbose_name=_("Parent Review")
    )
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")

    def __str__(self):
        return _("%(user)s rated %(target_type)s %(target_id)s (%(rating)s/5)") % {
            "user": self.user.email,
            "target_type": self.target_type,
            "target_id": self.target_id,
            "rating": self.rating,
        }
