from django.contrib import admin
from .models import PaymentMethod, PaymentTransaction, PaymentReceipt, Booking, Payout

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'method', 'amount', 'currency', 'status', 'purpose', 'reference', 'created')
    list_filter = ('status', 'method', 'currency', 'created', 'purpose')
    search_fields = ('user__email', 'reference', 'external_id', 'amount')
    date_hierarchy = 'created'
    ordering = ('-created',)

@admin.register(PaymentReceipt)
class PaymentReceiptAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'issued_at')
    search_fields = ('transaction__reference',)
    date_hierarchy = 'issued_at'
    ordering = ('-issued_at',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('learner_or_visitor', 'tutor', 'booking_type', 'is_paid_to_admin', 'created_at')
    list_filter = ('booking_type', 'is_paid_to_admin', 'created_at')
    search_fields = ('learner_or_visitor__email', 'tutor__email', 'booking_type')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

@admin.register(Payout)
class PayoutAdmin(admin.ModelAdmin):
    list_display = ('guide_or_tutor', 'amount', 'status', 'date', 'paid_by_admin')
    list_filter = ('status', 'date')
    search_fields = ('guide_or_tutor__email', 'related_booking__id', 'amount')
    date_hierarchy = 'date'
    ordering = ('-date',)