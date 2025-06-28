from django.db import models
from django.conf import settings
from villages.models import Village

class TouristicAttraction(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    village = models.ForeignKey(Village, related_name='attractions', on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    main_image = models.ImageField(upload_to="tourism/attractions/", null=True, blank=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="attractions_added")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class SocialImmersionExperience(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    village = models.ForeignKey(Village, related_name='social_immersions', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    host_family = models.CharField(max_length=255, blank=True)
    activities = models.TextField(help_text="Describe the activities involved", blank=True)
    live_cooking = models.BooleanField(default=False)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="social_immersions_added")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class HostingFamilyExperience(models.Model):
    family_name = models.CharField(max_length=255)
    description = models.TextField()
    village = models.ForeignKey(Village, related_name='hosting_families', on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    contact = models.CharField(max_length=255, blank=True)
    can_host = models.PositiveIntegerField(default=1, help_text="How many tourists can be hosted")
    live_cooking = models.BooleanField(default=False)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='families_added')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.family_name

class TourismActivity(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    attraction = models.ForeignKey(
        TouristicAttraction, related_name='activities', on_delete=models.CASCADE, null=True, blank=True
    )
    immersion = models.ForeignKey(
        SocialImmersionExperience, related_name='tourism_activities', on_delete=models.CASCADE, null=True, blank=True
    )
    family = models.ForeignKey(
        HostingFamilyExperience, related_name='tourism_activities', on_delete=models.CASCADE, null=True, blank=True
    )
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TouristFeedback(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Feedback on which experience?
    attraction = models.ForeignKey(TouristicAttraction, related_name="feedbacks", on_delete=models.CASCADE, null=True, blank=True)
    immersion = models.ForeignKey(SocialImmersionExperience, related_name="feedbacks", on_delete=models.CASCADE, null=True, blank=True)
    family = models.ForeignKey(HostingFamilyExperience, related_name="feedbacks", on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user} ({self.rating})"

class TouristComment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # Generic relation: link to any tourism object
    attraction = models.ForeignKey(TouristicAttraction, related_name="comments", on_delete=models.CASCADE, null=True, blank=True)
    immersion = models.ForeignKey(SocialImmersionExperience, related_name="comments", on_delete=models.CASCADE, null=True, blank=True)
    family = models.ForeignKey(HostingFamilyExperience, related_name="comments", on_delete=models.CASCADE, null=True, blank=True)

class SharedTouristMedia(models.Model):
    image = models.ImageField(upload_to="tourism/shared_media/", null=True, blank=True)
    video = models.FileField(upload_to="tourism/shared_media/videos/", null=True, blank=True)
    caption = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    attraction = models.ForeignKey(TouristicAttraction, related_name="shared_media", on_delete=models.CASCADE, null=True, blank=True)
    immersion = models.ForeignKey(SocialImmersionExperience, related_name="shared_media", on_delete=models.CASCADE, null=True, blank=True)
    family = models.ForeignKey(HostingFamilyExperience, related_name="shared_media", on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)