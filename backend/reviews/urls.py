from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ReviewViewSet
from . import views_classic

router = DefaultRouter()
router.register('reviews', ReviewViewSet, basename='review')

classic_urlpatterns = [
    path('classic/', views_classic.review_list, name='review_list'),
    path('classic/<int:pk>/', views_classic.review_detail, name='review_detail'),
    path('classic/create/', views_classic.review_create, name='review_create'),
    path('classic/<int:pk>/edit/', views_classic.review_edit, name='review_edit'),
]

urlpatterns = [
    path('', include(router.urls)),
    *classic_urlpatterns,
]