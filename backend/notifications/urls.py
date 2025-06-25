from django.urls import path
from .views import (
    NotificationListView,
    MarkAsReadView,
    MarkAsUnreadView,
    DeleteNotificationView,
    MarkAllNotificationsReadView,  # <-- Add this import
)

urlpatterns = [
    path('', NotificationListView.as_view(), name='notifications-list'),
    path('<int:pk>/read/', MarkAsReadView.as_view(), name='mark-as-read'),
    path('<int:pk>/unread/', MarkAsUnreadView.as_view(), name='mark-as-unread'),
    path('mark-all-read/', MarkAllNotificationsReadView.as_view(), name='mark_all_read'),  # <-- Use direct reference
    path('<int:pk>/delete/', DeleteNotificationView.as_view(), name='delete-notification'),
]
