from rest_framework import serializers
from .models import Payment, Booking, Payout
from django.contrib.contenttypes.models import ContentType
from tutorials.models import Tutorial

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = [
            'learner_or_visitor',
            'is_paid_to_admin',
            'is_paid_to_service_provider',
            'created_at'
        ]


class PaymentSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='payer.email', read_only=True)
    content_type = serializers.SlugRelatedField(
        queryset=ContentType.objects.all(),
        slug_field='model',
        required=False
    )
    related_object = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = [
            'id',
            'payer',
            'user_email',
            'amount',
            'payment_method',
            'transaction_id',
            'status',
            'purpose',
            'content_type',
            'object_id',
            'related_object',
            'timestamp',
            'description'
        ]
        read_only_fields = ['status', 'timestamp', 'related_object']

    def get_related_object(self, obj):
        if obj.related_object:
            if obj.purpose == "tutorial":
                try:
                    return obj.related_object.title
                except:
                    return str(obj.related_object)
            elif obj.purpose == "booking":
                try:
                    if hasattr(obj.related_object, 'tutor'):
                        name = obj.related_object.tutor or obj.related_object.guide
                        return f"Booking with {name} on {obj.related_object.date}"
                    return str(obj.related_object)
                except:
                    return str(obj.related_object)
        return None


class PayoutSerializer(serializers.ModelSerializer):
    guide_or_tutor_email = serializers.EmailField(source='guide_or_tutor.email', read_only=True)

    class Meta:
        model = Payout
        fields = [
            'id',
            'guide_or_tutor',
            'guide_or_tutor_email',
            'amount',
            'related_booking',
            'status',
            'date'
        ]
        read_only_fields = ['date']
