

from django.urls import path
from . import views


urlpatterns = [
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),

    path('attractions/', views.AttractionListCreateView.as_view(), name='attraction-list-create'),
    path('attractions/<int:pk>/', views.AttractionDetailView.as_view(), name='attraction-detail'),

    path('localsites/', views.LocalSiteListCreateView.as_view(), name='localsite-list-create'),
    path('localsites/<int:pk>/', views.LocalSiteDetailView.as_view(), name='localsite-detail'),

    path('tourplans/', views.TourPlanListCreateView.as_view(), name='tourplan-list-create'),
    path('tourplans/<int:pk>/', views.TourPlanDetailView.as_view(), name='tourplan-detail'),



]
