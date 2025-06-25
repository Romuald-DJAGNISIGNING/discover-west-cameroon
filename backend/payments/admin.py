from django.contrib import admin
from .models import Payment, Booking, Payout

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'payer', 'amount', 'status', 'payment_method', 'purpose', 'timestamp')
    list_filter = ('status', 'payment_method', 'purpose')
    search_fields = ('payer__email', 'transaction_id', 'purpose')
    readonly_fields = ('timestamp',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'learner_or_visitor', 'tutor', 'guide', 'booking_type', 'is_paid_to_admin', 'is_paid_to_service_provider', 'created_at')
    list_filter = ('is_paid_to_admin', 'is_paid_to_service_provider', 'booking_type')
    search_fields = ('user__email',)

@admin.register(Payout)
class PayoutAdmin(admin.ModelAdmin):
    list_display = ('id', 'guide_or_tutor', 'amount', 'status', 'date')
    list_filter = ('status',)
    search_fields = ('guide_or_tutor__email',)
    readonly_fields = ('date',)
