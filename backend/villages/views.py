from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Village, VillageImage, VillageComment
from .serializers import VillageSerializer, VillageImageSerializer, VillageCommentSerializer
from .permissions import IsTutorOrGuideOrReadOnly


class VillageViewSet(viewsets.ModelViewSet):
    queryset = Village.objects.all().order_by('-id')
    serializer_class = VillageSerializer
    permission_classes = [IsTutorOrGuideOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'department', 'main_languages', 'description', 'cultural_highlights', 'traditional_foods', 'art_crafts']
    ordering_fields = ['name', 'population', 'tourism_status']

    @action(detail=True, methods=['get', 'post'], permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def comments(self, request, pk=None):
        village = self.get_object()
        if request.method == 'GET':
            comments = village.comments.all()
            serializer = VillageCommentSerializer(comments, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            data = request.data.copy()
            data['village'] = village.id
            data['user'] = request.user.id
            serializer = VillageCommentSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get', 'post'], permission_classes=[IsTutorOrGuideOrReadOnly])
    def images(self, request, pk=None):
        village = self.get_object()
        if request.method == 'GET':
            images = village.images.all()
            serializer = VillageImageSerializer(images, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            data = request.data.copy()
            data['village'] = village.id
            serializer = VillageImageSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VillageImageViewSet(viewsets.ModelViewSet):
    queryset = VillageImage.objects.all().order_by('-id')
    serializer_class = VillageImageSerializer
    permission_classes = [IsTutorOrGuideOrReadOnly]

    def create(self, request, *args, **kwargs):
        # Handle file upload separately
        data = request.data.copy()
        if 'village' not in data:
            return Response(
                {"village": "This field is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class VillageCommentViewSet(viewsets.ModelViewSet):
    queryset = VillageComment.objects.all().order_by('-created_at')
    serializer_class = VillageCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]