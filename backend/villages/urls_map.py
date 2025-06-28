from django.urls import path
from .views_map import village_map_view

urlpatterns = [
    path('villages/<int:pk>/map/', village_map_view, name='village-map-view'),
]