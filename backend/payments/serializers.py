from rest_framework import serializers
from .models import PaymentMethod, PaymentTransaction, PaymentReceipt, Booking, Payout
from django.contrib.auth import get_user_model

User = get_user_model()

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = "__all__"

class BookingSerializer(serializers.ModelSerializer):
    learner_or_visitor = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    tutor = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True)
    guide = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True)
    
    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = ('is_paid_to_admin', 'is_paid_to_service_provider', 'created_at')

class PaymentTransactionSerializer(serializers.ModelSerializer):
    method = PaymentMethodSerializer(read_only=True)
    method_id = serializers.PrimaryKeyRelatedField(
        queryset=PaymentMethod.objects.all(), source='method', write_only=True
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), default=serializers.CurrentUserDefault()
    )
    
    class Meta:
        model = PaymentTransaction
        fields = [
            "id", "user", "method", "method_id", "amount", "currency", "status", "purpose",
            "reference", "external_id", "created", "updated", "description", "metadata",
            "content_type", "object_id", "is_paid_to_admin"
        ]
        read_only_fields = ("status", "reference", "external_id", "created", "updated", "is_paid_to_admin")

    def validate(self, data):
        if data['amount'] <= 0:
            raise serializers.ValidationError("Amount must be greater than zero")
        return data

class PaymentReceiptSerializer(serializers.ModelSerializer):
    transaction = PaymentTransactionSerializer(read_only=True)
    
    class Meta:
        model = PaymentReceipt
        fields = "__all__"
        read_only_fields = ('issued_at',)

class PayoutSerializer(serializers.ModelSerializer):
    guide_or_tutor = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    related_booking = serializers.PrimaryKeyRelatedField(queryset=Booking.objects.all())
    paid_by_admin = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_staff=True), allow_null=True, required=False
    )
    
    class Meta:
        model = Payout
        fields = [
            "id", "guide_or_tutor", "amount", "status", "date", 
            "related_booking", "note", "paid_by_admin"
        ]
        read_only_fields = ("status", "date", "paid_by_admin")