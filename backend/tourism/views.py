

from rest_framework import generics
from .models import Category, Attraction, LocalSite, TourPlan
from .serializers import (
    CategorySerializer,
    AttractionSerializer,
    LocalSiteSerializer,
    TourPlanSerializer
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Category Views
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# Attraction Views
class AttractionListCreateView(generics.ListCreateAPIView):
    queryset = Attraction.objects.all()
    serializer_class = AttractionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class AttractionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attraction.objects.all()
    serializer_class = AttractionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# Local Site Views
class LocalSiteListCreateView(generics.ListCreateAPIView):
    queryset = LocalSite.objects.all()
    serializer_class = LocalSiteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class LocalSiteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LocalSite.objects.all()
    serializer_class = LocalSiteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# Tour Plan Views
class TourPlanListCreateView(generics.ListCreateAPIView):
    queryset = TourPlan.objects.all()
    serializer_class = TourPlanSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class TourPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TourPlan.objects.all()
    serializer_class = TourPlanSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


