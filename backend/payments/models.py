from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class PaymentMethod(models.TextChoices):
    ORANGE_MONEY = 'orange_money', _('Orange Money')
    MTN_MOBILE_MONEY = 'mtn_mobile_money', _('MTN Mobile Money')
    CARD = 'card', _('Card')
    PAYPAL = 'paypal', _('PayPal')  # Optional future extension

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PaymentMethod.choices)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, default='pending')  # Could be success, failed, pending
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.email} - {self.amount} {self.payment_method} - {self.status}"
