from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model
from .models import (
    Festival, FestivalMedia, FestivalFact, FestivalComment,
    FestivalBookmark, FestivalAttendance, FestivalFeedback
)
from .serializers import (
    FestivalSerializer, FestivalMediaSerializer, FestivalFactSerializer,
    FestivalCommentSerializer, FestivalAttendanceSerializer, FestivalFeedbackSerializer
)
from .permissions import IsTutorOrGuideOrReadOnly, IsAttendanceOwnerOrReadOnly

User = get_user_model()

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class FestivalViewSet(viewsets.ModelViewSet):
    queryset = Festival.objects.all().order_by('-created_at')
    serializer_class = FestivalSerializer
    permission_classes = [IsTutorOrGuideOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'village__name', 'type', 'main_language', 'main_ethnic_group']
    ordering_fields = ['start_date', 'name', 'popularity_score']
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def bookmark(self, request, pk=None):
        festival = self.get_object()
        bookmark, created = FestivalBookmark.objects.get_or_create(
            festival=festival, 
            user=request.user
        )
        if created:
            return Response({"status": "bookmarked"}, status=status.HTTP_200_OK)
        bookmark.delete()
        return Response({"status": "unbookmarked"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get', 'post'], permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def comments(self, request, pk=None):
        festival = self.get_object()
        if request.method == 'POST':
            serializer = FestivalCommentSerializer(
                data={'comment': request.data.get('comment')},
                context={'request': request, 'festival': festival}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user, festival=festival)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        comments = festival.comments.all().order_by('-created_at')
        page = self.paginate_queryset(comments)
        if page is not None:
            serializer = FestivalCommentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = FestivalCommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get', 'post'], permission_classes=[permissions.IsAuthenticated])
    def attendances(self, request, pk=None):
        festival = self.get_object()
        if request.method == 'POST':
            if FestivalAttendance.objects.filter(festival=festival, user=request.user).exists():
                return Response(
                    {'detail': 'You are already attending this festival.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            booked_tutor_guide_id = request.data.get('booked_tutor_guide')
            booked_tutor_guide = None
            if booked_tutor_guide_id:
                try:
                    booked_tutor_guide = User.objects.get(
                        pk=booked_tutor_guide_id,
                        role__in=['tutor', 'guide']
                    )
                except User.DoesNotExist:
                    return Response(
                        {'detail': 'Selected tutor/guide not found or invalid.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            attendance = FestivalAttendance.objects.create(
                festival=festival,
                user=request.user,
                booked_tutor_guide=booked_tutor_guide
            )
            serializer = FestivalAttendanceSerializer(attendance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        attendances = festival.attendances.all().order_by('-created_at')
        serializer = FestivalAttendanceSerializer(attendances, many=True)
        return Response(serializer.data)

class FestivalAttendanceViewSet(viewsets.ModelViewSet):
    queryset = FestivalAttendance.objects.all().order_by('-created_at')
    serializer_class = FestivalAttendanceSerializer
    permission_classes = [permissions.IsAuthenticated, IsAttendanceOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        attendance = self.get_object()
        status_choice = request.data.get('status')
        
        if status_choice not in dict(attendance.ATTENDANCE_STATUS_CHOICES):
            return Response(
                {'detail': 'Invalid status value.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        attendance.status = status_choice
        attendance.save()
        return Response(
            {'status': attendance.status},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def feedback(self, request, pk=None):
        attendance = self.get_object()
        
        if attendance.user != request.user:
            return Response(
                {'detail': 'You can only provide feedback for your own attendance.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        data = request.data.copy()
        data['attendance'] = attendance.id  # Ensure attendance is set
        
        if hasattr(attendance, 'feedback'):
            serializer = FestivalFeedbackSerializer(
                attendance.feedback,
                data=data,
                partial=True,
                context={'request': request}
            )
            status_code = status.HTTP_200_OK
        else:
            serializer = FestivalFeedbackSerializer(
                data=data,
                context={'request': request, 'attendance': attendance}
            )
            status_code = status.HTTP_201_CREATED
        
        serializer.is_valid(raise_exception=True)
        serializer.save(attendance=attendance)  # Explicitly set attendance
        return Response(serializer.data, status=status_code)

class FestivalFeedbackViewSet(viewsets.ModelViewSet):
    queryset = FestivalFeedback.objects.all().order_by('-created_at')
    serializer_class = FestivalFeedbackSerializer
    permission_classes = [permissions.IsAuthenticated, IsAttendanceOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(attendance__user=self.request.user)
        return queryset

class FestivalMediaViewSet(viewsets.ModelViewSet):
    queryset = FestivalMedia.objects.all().order_by('-created_at')
    serializer_class = FestivalMediaSerializer
    permission_classes = [IsTutorOrGuideOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        festival_id = self.request.data.get('festival')
        if not festival_id:
            raise serializers.ValidationError({'festival': 'This field is required.'})
        
        try:
            festival = Festival.objects.get(pk=festival_id)
        except Festival.DoesNotExist:
            raise serializers.ValidationError({'festival': 'Invalid festival ID.'})
        
        # Ensure image is in request.FILES
        if 'image' not in self.request.FILES:
            raise serializers.ValidationError({'image': 'This field is required.'})
        
        serializer.save(
            festival=festival,
            image=self.request.FILES['image']
        )

class FestivalFactViewSet(viewsets.ModelViewSet):
    queryset = FestivalFact.objects.all().order_by('-created_at')
    serializer_class = FestivalFactSerializer
    permission_classes = [IsTutorOrGuideOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        festival_id = self.request.data.get('festival')
        if not festival_id:
            raise serializers.ValidationError({'festival': 'This field is required.'})
        serializer.save(festival_id=festival_id)