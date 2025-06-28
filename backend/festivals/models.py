from django.db import models
from django.conf import settings
from django.db.models import Avg

class Festival(models.Model):
    FESTIVAL_TYPE_CHOICES = (
        ('traditional', 'Traditional'),
        ('modern', 'Modern'),
        ('religious', 'Religious'),
        ('other', 'Other'),
    )
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    type = models.CharField(max_length=32, choices=FESTIVAL_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255)
    village = models.ForeignKey('villages.Village', null=True, blank=True, on_delete=models.SET_NULL, related_name='festivals')
    main_language = models.CharField(max_length=64, default="French")
    main_ethnic_group = models.CharField(max_length=64, blank=True)
    traditional_foods = models.TextField(blank=True)
    main_activities = models.TextField(blank=True)
    is_annual = models.BooleanField(default=True)
    website = models.URLField(blank=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='festivals_added')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def average_rating(self):
        avg = self.feedbacks.aggregate(Avg('rating'))['rating__avg']
        return round(avg or 0, 2) if avg is not None else 0.0

    @property
    def popularity_score(self):
        confirmed = self.attendances.filter(status='confirmed').count()
        avg_rating = self.average_rating
        return round(confirmed * (avg_rating / 5.0), 2)

    class Meta:
        ordering = ['-created_at']

class FestivalMedia(models.Model):
    festival = models.ForeignKey(Festival, related_name='media', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='festivals/images/', blank=True, null=True)
    video_url = models.URLField(blank=True)
    caption = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

class FestivalFact(models.Model):
    festival = models.ForeignKey(Festival, related_name='facts', on_delete=models.CASCADE)
    fact = models.CharField(max_length=255)
    source = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

class FestivalBookmark(models.Model):
    festival = models.ForeignKey(Festival, related_name='bookmarks', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('festival', 'user')
        ordering = ['-created_at']

class FestivalAttendance(models.Model):
    ATTENDANCE_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='festival_attendances')
    festival = models.ForeignKey(Festival, related_name='attendances', on_delete=models.CASCADE)
    status = models.CharField(max_length=16, choices=ATTENDANCE_STATUS_CHOICES, default='pending')
    booked_tutor_guide = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='booked_attendances')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'festival')
        ordering = ['-created_at']

class FestivalFeedback(models.Model):
    attendance = models.OneToOneField(
        FestivalAttendance, 
        related_name='feedback', 
        on_delete=models.CASCADE
    )
    festival = models.ForeignKey(
        Festival,
        related_name='feedbacks',
        on_delete=models.CASCADE,
        null=True
    )
    feedback_text = models.TextField(blank=True)
    rating = models.PositiveSmallIntegerField()
    image = models.ImageField(upload_to='festivals/feedback/images/', blank=True, null=True)
    video_url = models.URLField(blank=True)
    experience = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.festival_id and self.attendance_id:
            self.festival = self.attendance.festival
        super().save(*args, **kwargs)

class FestivalComment(models.Model):
    festival = models.ForeignKey(Festival, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']