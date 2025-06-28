from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import VillageViewSet, VillageImageViewSet, VillageCommentViewSet
from .views_map import village_map_view

router = DefaultRouter()
router.register('villages', VillageViewSet, basename='village')
router.register('village-images', VillageImageViewSet, basename='villageimage')
router.register('village-comments', VillageCommentViewSet, basename='villagecomment')

urlpatterns = [
    path('', include(router.urls)),
    # Map view for a single village (returns the Leaflet map page)
    path('villages/<int:pk>/map/', village_map_view, name='village-map-view'),
]