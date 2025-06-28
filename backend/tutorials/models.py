from django.db import models
from django.conf import settings
from villages.models import Village
from tourism.models import TouristicAttraction
from festivals.models import Festival

class TutorialCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name

class Tutorial(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(TutorialCategory, related_name="tutorials", on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True)
    content = models.TextField()
    video_url = models.URLField(blank=True)
    pdf_file = models.FileField(upload_to="tutorials/pdfs/", blank=True, null=True)
    image = models.ImageField(upload_to="tutorials/images/", blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    village = models.ForeignKey(Village, null=True, blank=True, on_delete=models.SET_NULL, related_name="tutorials")
    attraction = models.ForeignKey(TouristicAttraction, null=True, blank=True, on_delete=models.SET_NULL, related_name="tutorials")
    festival = models.ForeignKey(Festival, null=True, blank=True, on_delete=models.SET_NULL, related_name="tutorials")
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class TutorialComment(models.Model):
    tutorial = models.ForeignKey(Tutorial, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.user.username} on {self.tutorial.title}"