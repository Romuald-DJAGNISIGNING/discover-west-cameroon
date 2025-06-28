from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ReportViewSet
from . import views_classic

router = DefaultRouter()
router.register('reports', ReportViewSet, basename='report')

classic_urlpatterns = [
    path('classic/', views_classic.report_list, name='report_list'),
    path('classic/<int:pk>/', views_classic.report_detail, name='report_detail'),
    path('classic/create/', views_classic.report_create, name='report_create'),
    path('classic/<int:pk>/edit/', views_classic.report_edit, name='report_edit'),
    path('classic/<int:pk>/review/', views_classic.report_review, name='report_review'),
]

urlpatterns = [
    path('', include(router.urls)),
    *classic_urlpatterns,
]