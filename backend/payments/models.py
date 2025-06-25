from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal
from users.models import CustomUser

User = get_user_model()


class Booking(models.Model):
    learner_or_visitor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Booked User"))
    tutor = models.ForeignKey(
        User, null=True, blank=True, related_name="tutor_bookings", on_delete=models.SET_NULL, verbose_name=_("Tutor")
    )
    guide = models.ForeignKey(
        User, null=True, blank=True, related_name="guide_bookings", on_delete=models.SET_NULL, verbose_name=_("Guide")
    )
    booking_type = models.CharField(max_length=100, verbose_name=_("Service Type"))
    is_paid_to_admin = models.BooleanField(default=False, verbose_name=_("Is Paid to Admin"))
    is_paid_to_service_provider = models.BooleanField(default=False, verbose_name=_("Is Paid to Service Provider"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    def __str__(self):
        return f"{_('Booking by')} {self.learner_or_visitor} {_('for')} {self.booking_type}"

    class Meta:
        verbose_name = _("Booking")
        verbose_name_plural = _("Bookings")


class Payment(models.Model):
    PAYMENT_METHODS = (
        ('orange', _("Orange Money")),
        ('mtn', _("MTN Mobile Money")),
        ('paypal', _("PayPal")),
        ('card', _("Card")),
    )
    PURPOSE_CHOICES = (
        ('tutorial', _("Tutorial")),
        ('booking', _("Booking")),
        ('other', _("Other")),
    )

    payer = models.ForeignKey(User, related_name='payments', on_delete=models.CASCADE, verbose_name=_("User"))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Amount"))
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, verbose_name=_("Payment Method"))
    transaction_id = models.CharField(max_length=100, unique=True, verbose_name=_("Transaction ID"))
    status = models.CharField(
        max_length=20,
        choices=(('pending', _("Pending")), ('completed', _("Completed"))),
        default='pending',
        verbose_name=_("Status")
    )
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES, verbose_name=_("Purpose"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))

    # Generic relation to the related object (e.g. Tutorial, Booking, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("Target Type"))
    object_id = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Target ID"))
    related_object = GenericForeignKey('content_type', 'object_id')

    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_("Timestamp"))

    def __str__(self):
        return f"{self.payer} - {self.amount} FCFA - {self.get_status_display()}"

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")


class Payout(models.Model):
    guide_or_tutor = models.ForeignKey(User, related_name='payouts', on_delete=models.CASCADE, verbose_name=_("Guide or Tutor"))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Amount Paid"))
    related_booking = models.ForeignKey(Booking, related_name='payouts', on_delete=models.CASCADE, verbose_name=_("Booking"))
    status = models.CharField(
        max_length=20,
        choices=(('pending', _("Pending")), ('paid', _("Paid"))),
        default='pending',
        verbose_name=_("Status")
    )
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))

    def __str__(self):
        return f"{_('Payout to')} {self.guide_or_tutor} - {self.amount} FCFA"

    class Meta:
        verbose_name = _("Payout")
        verbose_name_plural = _("Payouts")
