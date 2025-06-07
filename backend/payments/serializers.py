
from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id',
            'user',
            'user_email',
            'amount',
            'payment_method',
            'transaction_id',
            'status',
            'timestamp',
            'description'
        ]
        read_only_fields = ['status', 'timestamp']
