from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import SupportTicketViewSet, SupportMessageViewSet
from . import views_classic

router = DefaultRouter()
router.register('support-tickets', SupportTicketViewSet, basename='supportticket')
router.register('support-messages', SupportMessageViewSet, basename='supportmessage')

classic_urlpatterns = [
    path('classic/', views_classic.ticket_list, name='support_ticket_list'),
    path('classic/<int:pk>/', views_classic.ticket_detail, name='support_ticket_detail'),
    path('classic/create/', views_classic.ticket_create, name='support_ticket_create'),
    path('classic/<int:pk>/assign/', views_classic.ticket_assign, name='support_ticket_assign'),
    path('classic/<int:pk>/resolve/', views_classic.ticket_resolve, name='support_ticket_resolve'),
]

urlpatterns = [
    path('', include(router.urls)),
    *classic_urlpatterns,
]