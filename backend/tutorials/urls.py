from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
from . import views_classic

# API Router Configuration
router = DefaultRouter()
router.register(r'tutorials', views.TutorialViewSet, basename='tutorial')
router.register(r'categories', views.TutorialCategoryViewSet, basename='tutorialcategory')
router.register(r'comments', views.TutorialCommentViewSet, basename='tutorialcomment')

# Classic (Template-based) Views
classic_patterns = [
    path('', views_classic.tutorial_list, name='tutorial-list-classic'),
    path('<int:pk>/', views_classic.tutorial_detail, name='tutorial-detail-classic'),
    path('create/', views_classic.tutorial_create, name='tutorial-create-classic'),
    path('<int:pk>/edit/', views_classic.tutorial_edit, name='tutorial-edit-classic'),
]

# API Custom Endpoints
api_patterns = [
path('tutorials/<int:tutorial_id>/add-comment/',
        views.TutorialCommentViewSet.as_view({'post': 'create'}),
        name='tutorial-add-comment'),
]

urlpatterns = [
    # API endpoints
    path('', include(router.urls)),
    path('', include(api_patterns)),
    
    # Classic HTML endpoints
    path('classic/', include(classic_patterns)),
]

app_name = 'tutorials'  # Single app namespace