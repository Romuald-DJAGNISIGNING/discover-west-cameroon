from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import (
    TouristicAttraction, SocialImmersionExperience, HostingFamilyExperience,
    TourismActivity, TouristFeedback, TouristComment, SharedTouristMedia
)
from .serializers import (
    TouristicAttractionSerializer, SocialImmersionExperienceSerializer, HostingFamilyExperienceSerializer,
    TourismActivitySerializer, TouristFeedbackSerializer, TouristCommentSerializer, SharedTouristMediaSerializer
)
from .permissions import IsGuideOrTutorOrReadOnly

class BaseTourismViewSet(viewsets.ModelViewSet):
    def get_parent_field_name(self):
        if isinstance(self, TouristicAttractionViewSet):
            return 'attraction'
        elif isinstance(self, SocialImmersionExperienceViewSet):
            return 'immersion'
        elif isinstance(self, HostingFamilyExperienceViewSet):
            return 'family'
        return None

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_feedback(self, request, pk=None):
        parent = self.get_object()
        data = request.data.copy()
        data.update({
            'user': request.user.id,
            self.get_parent_field_name(): parent.id
        })
        serializer = TouristFeedbackSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_comment(self, request, pk=None):
        parent = self.get_object()
        data = request.data.copy()
        data.update({
            'user': request.user.id,
            self.get_parent_field_name(): parent.id
        })
        serializer = TouristCommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_media(self, request, pk=None):
        parent = self.get_object()
        data = request.data.copy()
        data[self.get_parent_field_name()] = parent.id
        
        serializer = SharedTouristMediaSerializer(
            data=data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TouristicAttractionViewSet(BaseTourismViewSet):
    queryset = TouristicAttraction.objects.all()
    serializer_class = TouristicAttractionSerializer
    permission_classes = [IsGuideOrTutorOrReadOnly]
    filterset_fields = ['village']

class SocialImmersionExperienceViewSet(BaseTourismViewSet):
    queryset = SocialImmersionExperience.objects.all()
    serializer_class = SocialImmersionExperienceSerializer
    permission_classes = [IsGuideOrTutorOrReadOnly]
    filterset_fields = ['village']

class HostingFamilyExperienceViewSet(BaseTourismViewSet):
    queryset = HostingFamilyExperience.objects.all()
    serializer_class = HostingFamilyExperienceSerializer
    permission_classes = [IsGuideOrTutorOrReadOnly]
    filterset_fields = ['village']

class TourismActivityViewSet(viewsets.ModelViewSet):
    queryset = TourismActivity.objects.all()
    serializer_class = TourismActivitySerializer
    permission_classes = [IsGuideOrTutorOrReadOnly]

class TouristFeedbackViewSet(viewsets.ModelViewSet):
    queryset = TouristFeedback.objects.all()
    serializer_class = TouristFeedbackSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class TouristCommentViewSet(viewsets.ModelViewSet):
    queryset = TouristComment.objects.all()
    serializer_class = TouristCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SharedTouristMediaViewSet(viewsets.ModelViewSet):
    queryset = SharedTouristMedia.objects.all()
    serializer_class = SharedTouristMediaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]