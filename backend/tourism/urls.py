from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    TouristicAttractionViewSet, SocialImmersionExperienceViewSet, HostingFamilyExperienceViewSet,
    TourismActivityViewSet, TouristFeedbackViewSet, TouristCommentViewSet, SharedTouristMediaViewSet
)

router = DefaultRouter()
router.register('attractions', TouristicAttractionViewSet, basename='attraction')
router.register('social-immersions', SocialImmersionExperienceViewSet, basename='socialimmersion')
router.register('hosting-families', HostingFamilyExperienceViewSet, basename='hostingfamily')
router.register('activities', TourismActivityViewSet, basename='tourismactivity')
router.register('feedbacks', TouristFeedbackViewSet, basename='touristfeedback')
router.register('comments', TouristCommentViewSet, basename='touristcomment')
router.register('shared-media', SharedTouristMediaViewSet, basename='sharedmedia')

urlpatterns = [
    path('', include(router.urls)),
]