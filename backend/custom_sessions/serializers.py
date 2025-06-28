from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CustomSession, SessionMaterial, SessionFeedback, InAppNotification

User = get_user_model()

class SessionMaterialSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = SessionMaterial
        fields = "__all__"
        read_only_fields = ("uploaded_at", "uploaded_by")

class SessionFeedbackSerializer(serializers.ModelSerializer):
    session = serializers.PrimaryKeyRelatedField(queryset=CustomSession.objects.all())
    author = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), read_only=True)
    
    class Meta:
        model = SessionFeedback
        fields = "__all__"
        read_only_fields = ("author", "created_at")
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=SessionFeedback.objects.all(),
                fields=('session', 'author'),
                message="You have already submitted feedback for this session."
            )
        ]

    def validate(self, data):
        request = self.context.get('request')
        session = data.get('session')
        
        if not session.can_accept_feedback():
            raise serializers.ValidationError(
                {"session": "Feedback can only be submitted for completed sessions"}
            )
            
        if request and request.user not in [session.tutor_or_guide, session.learner_or_visitor]:
            raise serializers.ValidationError(
                {"author": "Only session participants can submit feedback"}
            )
            
        if data.get('rating', 0) not in range(1, 6):
            raise serializers.ValidationError({
                'rating': 'Rating must be between 1 and 5'
            })
            
        return data

    def create(self, validated_data):
        feedback = super().create(validated_data)
        
        # Create notifications for both participants
        session = validated_data['session']
        InAppNotification.objects.create(
            user=session.tutor_or_guide,
            message=f"New feedback received for your session: {session.topic_or_location}"
        )
        InAppNotification.objects.create(
            user=session.learner_or_visitor,
            message=f"Your feedback has been submitted for: {session.topic_or_location}"
        )
        
        return feedback

class CustomSessionSerializer(serializers.ModelSerializer):
    materials = SessionMaterialSerializer(many=True, read_only=True)
    feedbacks = SessionFeedbackSerializer(many=True, read_only=True)
    tutor_or_guide = serializers.PrimaryKeyRelatedField(read_only=True)
    learner_or_visitor = serializers.PrimaryKeyRelatedField(read_only=True)
    status = serializers.CharField(read_only=True)
    is_confirmed = serializers.BooleanField(read_only=True)
    tutor_or_guide_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role__in=['tutor', 'guide']),
        source='tutor_or_guide',
        write_only=True,
        required=True
    )

    class Meta:
        model = CustomSession
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at", "learner_or_visitor")

    def validate(self, data):
        request = self.context.get('request')
        if request and request.method == 'POST':
            user = request.user
            session_type = data.get('session_type')
            
            if session_type == 'tutoring' and getattr(user, 'role', None) != 'learner':
                raise serializers.ValidationError("Only learners can create tutoring sessions")
            if session_type == 'tour_guide' and getattr(user, 'role', None) != 'visitor':
                raise serializers.ValidationError("Only visitors can create tour guide sessions")
        
        return data

    def create(self, validated_data):
        validated_data['learner_or_visitor'] = self.context['request'].user
        return super().create(validated_data)

class InAppNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InAppNotification
        fields = "__all__"
        read_only_fields = ("created_at", "user")