
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Village, Attraction, LocalSite
from .serializers import VillageSerializer, AttractionSerializer, LocalSiteSerializer

class VillageListView(APIView):
    def get(self, request):
        villages = Village.objects.all()
        serializer = VillageSerializer(villages, many=True)
        return Response(serializer.data)

class AttractionListView(APIView):
    def get(self, request):
        attractions = Attraction.objects.all()
        serializer = AttractionSerializer(attractions, many=True)
        return Response(serializer.data)

class LocalSiteListView(APIView):
    def get(self, request):
        local_sites = LocalSite.objects.all()
        serializer = LocalSiteSerializer(local_sites, many=True)
        return Response(serializer.data)
