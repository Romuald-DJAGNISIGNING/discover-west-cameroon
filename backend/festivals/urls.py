
from django.urls import path
from .views import FestivalListCreateView, FestivalDetailView

urlpatterns = [
    path('', FestivalListCreateView.as_view(), name='festival-list-create'),
    path('<int:pk>/', FestivalDetailView.as_view(), name='festival-detail'),
]
