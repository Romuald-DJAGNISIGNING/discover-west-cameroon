from rest_framework import serializers
from .models import Review

class RecursiveReviewSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class ReviewSerializer(serializers.ModelSerializer):
    replies = RecursiveReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'target_type', 'target_id', 'rating', 'comment', 'parent', 'replies', 'created_at']
        read_only_fields = ['user', 'created_at']
