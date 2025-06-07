from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'payment_method', 'status', 'timestamp')
    list_filter = ('payment_method', 'status', 'timestamp')
    search_fields = ('user__email', 'user__username')
