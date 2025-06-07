
from django.db import models

class Festival(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    image = models.ImageField(upload_to='festival_images/', null=True, blank=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name

