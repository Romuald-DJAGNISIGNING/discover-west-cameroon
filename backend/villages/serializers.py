
from rest_framework import serializers
from .models import Village, Attraction, LocalSite

class VillageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Village
        fields = ['id', 'name', 'location', 'population', 'tourism_status']

class AttractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attraction
        fields = ['id', 'name', 'village', 'attraction_type', 'description', 'tourist_rating']

class LocalSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalSite
        fields = ['id', 'name', 'village', 'site_type', 'description']
