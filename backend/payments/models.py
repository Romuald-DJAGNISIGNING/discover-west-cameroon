from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

User = get_user_model()

class Booking(models.Model):
    learner_or_visitor = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("Booked User"))
    tutor = models.ForeignKey(
        User, null=True, blank=True, related_name="tutor_bookings", 
        on_delete=models.SET_NULL, verbose_name=_("Tutor"))
    guide = models.ForeignKey(
        User, null=True, blank=True, related_name="guide_bookings", 
        on_delete=models.SET_NULL, verbose_name=_("Guide"))
    booking_type = models.CharField(max_length=100, verbose_name=_("Service Type"))
    is_paid_to_admin = models.BooleanField(default=False, verbose_name=_("Is Paid to Admin"))
    is_paid_to_service_provider = models.BooleanField(
        default=False, verbose_name=_("Is Paid to Service Provider"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    def __str__(self):
        return f"{_('Booking by')} {self.learner_or_visitor} {_('for')} {self.booking_type}"

    class Meta:
        verbose_name = _("Booking")
        verbose_name_plural = _("Bookings")
        ordering = ['-created_at']

class PaymentMethod(models.Model):
    METHOD_CHOICES = [
        ('orange', _("Orange Money")),
        ('mtn', _("MTN Mobile Money")),
        ('card', _("Credit Card")),
        ('paypal', _("PayPal")),
    ]
    name = models.CharField(max_length=50, choices=METHOD_CHOICES, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Payment Method")
        verbose_name_plural = _("Payment Methods")
        ordering = ['name']

    def __str__(self):
        return self.get_name_display()

class PaymentTransaction(models.Model):
    STATUS_CHOICES = [
        ('pending', _("Pending")),
        ('success', _("Success")),
        ('failed', _("Failed")),
        ('cancelled', _("Cancelled")),
    ]
    PURPOSE_CHOICES = (
        ('tutorial', _("Tutorial")),
        ('booking', _("Booking")),
        ('other', _("Other")),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='payments', verbose_name=_("User"))
    method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT, verbose_name=_("Payment Method"))
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Amount"))
    currency = models.CharField(max_length=8, default="XAF", verbose_name=_("Currency"))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name=_("Status"))
    reference = models.CharField(max_length=128, unique=True, verbose_name=_("Reference"))
    external_id = models.CharField(max_length=128, blank=True, null=True, verbose_name=_("External Transaction ID"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES, verbose_name=_("Purpose"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    metadata = models.JSONField(default=dict, blank=True, verbose_name=_("Metadata"))

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("Target Type"))
    object_id = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Target ID"))
    related_object = GenericForeignKey('content_type', 'object_id')

    is_paid_to_admin = models.BooleanField(default=True, verbose_name=_("Paid to Admin"))

    def __str__(self):
        return f"{self.user} - {self.amount} {self.currency} - {self.get_status_display()}"

    def clean(self):
        super().clean()
        
        # Common validations for all payment methods
        if self.amount <= 0:
            raise ValidationError(_("Amount must be greater than zero"))
        
        if not self.reference:
            raise ValidationError(_("Reference is required for all transactions"))
        
        # Method-specific validations
        if self.method.name == 'mtn':
            self._validate_mtn_transaction()
        elif self.method.name == 'orange':
            self._validate_orange_transaction()
        elif self.method.name == 'card':
            self._validate_card_transaction()
        elif self.method.name == 'paypal':
            self._validate_paypal_transaction()
    
    def _validate_mtn_transaction(self):
        """Validate MTN Mobile Money specific requirements"""
        if not isinstance(self.metadata, dict):
            raise ValidationError(_("Metadata must be a dictionary for MTN payments"))
        
        payer_phone = self.metadata.get('payer_phone')
        if not payer_phone:
            raise ValidationError(_("MTN payments require 'payer_phone' in metadata"))
        
        if not (payer_phone.startswith('6') and len(payer_phone) == 9 and payer_phone.isdigit()):
            raise ValidationError(_("Invalid MTN phone number format. Should be 9 digits starting with 6"))
        
        if self.currency != 'XAF':
            raise ValidationError(_("MTN payments only support XAF currency"))

    def _validate_orange_transaction(self):
        """Validate Orange Money specific requirements"""
        if not isinstance(self.metadata, dict):
            raise ValidationError(_("Metadata must be a dictionary for Orange payments"))
        
        if not self.metadata.get('notif_url'):
            raise ValidationError(_("Orange payments require 'notif_url' in metadata"))
        
        if not self.metadata.get('return_url'):
            raise ValidationError(_("Orange payments require 'return_url' in metadata"))
        
        if self.currency != 'XAF':
            raise ValidationError(_("Orange payments only support XAF currency"))

    def _validate_card_transaction(self):
        """Validate Credit Card (Stripe) specific requirements"""
        if not isinstance(self.metadata, dict):
            raise ValidationError(_("Metadata must be a dictionary for card payments"))
        
        if not self.metadata.get('stripe_token'):
            raise ValidationError(_("Card payments require 'stripe_token' in metadata"))
        
        # Validate currency is supported by Stripe
        supported_currencies = ['XAF', 'USD', 'EUR', 'GBP']
        if self.currency not in supported_currencies:
            raise ValidationError(_(f"Card payments only support these currencies: {', '.join(supported_currencies)}"))

    def _validate_paypal_transaction(self):
        """Validate PayPal specific requirements"""
        if not isinstance(self.metadata, dict):
            raise ValidationError(_("Metadata must be a dictionary for PayPal payments"))
        
        if not self.metadata.get('return_url'):
            raise ValidationError(_("PayPal payments require 'return_url' in metadata"))
        
        if not self.metadata.get('cancel_url'):
            raise ValidationError(_("PayPal payments require 'cancel_url' in metadata"))
        
        # Validate currency is supported by PayPal
        supported_currencies = ['XAF', 'USD', 'EUR', 'GBP']
        if self.currency not in supported_currencies:
            raise ValidationError(_(f"PayPal payments only support these currencies: {', '.join(supported_currencies)}"))

    def save(self, *args, **kwargs):
        """Override save to always call clean()"""
        self.full_clean()
        super().save(*args, **kwargs)   


    class Meta:
        ordering = ['-created']
        verbose_name = _("Payment Transaction")
        verbose_name_plural = _("Payment Transactions")

class PaymentReceipt(models.Model):
    transaction = models.OneToOneField(
        PaymentTransaction, on_delete=models.CASCADE, related_name='receipt')
    receipt_file = models.FileField(upload_to='payment_receipts/', blank=True, null=True)
    issued_at = models.DateTimeField(default=timezone.now)
    note = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _("Payment Receipt")
        verbose_name_plural = _("Payment Receipts")
        ordering = ['-issued_at']

    def __str__(self):
        return f"{_('Receipt for')} {self.transaction.reference}"

class Payout(models.Model):
    STATUS_CHOICES = (
        ('pending', _("Pending")),
        ('paid', _("Paid")),
        ('failed', _("Failed")),
    )
    guide_or_tutor = models.ForeignKey(
        User, related_name='payouts', on_delete=models.CASCADE, verbose_name=_("Guide or Tutor"))
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Amount Paid"))
    related_booking = models.ForeignKey(
        Booking, related_name='payouts', on_delete=models.CASCADE, verbose_name=_("Booking"))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name=_("Status"))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))
    note = models.TextField(blank=True, null=True, verbose_name=_("Note"))

    paid_by_admin = models.ForeignKey(
        User, related_name='admin_payouts', on_delete=models.SET_NULL,
        verbose_name=_("Paid by Admin"), null=True, blank=True
    )

    def __str__(self):
        return f"{_('Payout to')} {self.guide_or_tutor} - {self.amount} {self.related_booking}"

    class Meta:
        verbose_name = _("Payout")
        verbose_name_plural = _("Payouts")
        ordering = ['-date']