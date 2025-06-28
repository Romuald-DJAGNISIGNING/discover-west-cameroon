from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import (
    UserActivityLog, DailySiteStatistics, TourBookingStatistic,
    TutorBookingStatistic, GuideBookingStatistic
)

@receiver(post_save, sender=UserActivityLog)
def update_active_users_on_login(sender, instance, created, **kwargs):
    if created and instance.action == "login":
        today = timezone.now().date()
        stats, _ = DailySiteStatistics.objects.get_or_create(date=today)
        stats.active_users = stats.active_users + 1
        stats.save()

@receiver(post_save, sender=TourBookingStatistic)
def update_tour_booking_summary(sender, instance, created, **kwargs):
    if created:
        today = instance.date
        stats, _ = DailySiteStatistics.objects.get_or_create(date=today)
        stats.total_tour_bookings = stats.total_tour_bookings + instance.bookings_count
        stats.total_bookings = stats.total_bookings + instance.bookings_count
        stats.save()

@receiver(post_save, sender=TutorBookingStatistic)
def update_tutor_booking_summary(sender, instance, created, **kwargs):
    if created:
        today = instance.date
        stats, _ = DailySiteStatistics.objects.get_or_create(date=today)
        stats.total_tutor_bookings = stats.total_tutor_bookings + instance.bookings_count
        stats.total_bookings = stats.total_bookings + instance.bookings_count
        stats.save()

@receiver(post_save, sender=GuideBookingStatistic)
def update_guide_booking_summary(sender, instance, created, **kwargs):
    if created:
        today = instance.date
        stats, _ = DailySiteStatistics.objects.get_or_create(date=today)
        stats.total_guide_bookings = stats.total_guide_bookings + instance.bookings_count
        stats.total_bookings = stats.total_bookings + instance.bookings_count
        stats.save()