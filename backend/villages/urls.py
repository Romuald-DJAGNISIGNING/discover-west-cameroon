
from django.urls import path
from . import views

urlpatterns = [
    path('villages/', views.VillageListView.as_view(), name='village_list'),
    path('attractions/', views.AttractionListView.as_view(), name='attraction_list'),
    path('local-sites/', views.LocalSiteListView.as_view(), name='local_site_list'),
]
