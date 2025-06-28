from django.db import models
from django.conf import settings

class Village(models.Model):
    TOURISM_STATUS_CHOICES = (
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
        ('unknown', 'Unknown'),
    )

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    department = models.CharField(max_length=255, help_text="Department in the West Region")
    population = models.PositiveIntegerField(null=True, blank=True)
    tourism_status = models.CharField(max_length=16, choices=TOURISM_STATUS_CHOICES, default="unknown")
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    main_languages = models.CharField(max_length=255, help_text="Comma-separated list", blank=True)
    traditional_foods = models.TextField(blank=True)
    cultural_highlights = models.TextField(blank=True)
    art_crafts = models.TextField(blank=True)
    learn_more = models.TextField(blank=True, help_text="What can you learn about this village?")
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="villages_added")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name

class VillageImage(models.Model):
    village = models.ForeignKey(Village, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="villages/images/")
    caption = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-id']

class VillageComment(models.Model):
    village = models.ForeignKey(Village, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']