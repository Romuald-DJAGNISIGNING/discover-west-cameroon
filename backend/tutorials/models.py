from django.db import models
from django.conf import settings

class Tutorial(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tutorials'
    )
    category = models.ForeignKey(
        'TutorialCategory',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tutorials'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)  # <-- Add this line
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class TutorialStep(models.Model):
    tutorial = models.ForeignKey(
        Tutorial,
        on_delete=models.CASCADE,
        related_name='steps'
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    step_number = models.PositiveIntegerField()

    class Meta:
        ordering = ['step_number']

    def __str__(self):
        return f"{self.tutorial.title} - Step {self.step_number}"

class TutorialCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Ensures category names are unique
    description = models.TextField(blank=True, null=True)  # Optional description for the category
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically sets the creation timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Automatically updates the timestamp on changes

    class Meta:
        ordering = ['name']  
        verbose_name = "Tutorial Category"  
        verbose_name_plural = "Tutorial Categories"  
        
    def __str__(self):
        return self.name  

    def get_tutorial_count(self):
        """Returns the number of tutorials associated with this category."""
        return self.tutorials.count()