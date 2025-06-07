from django.db import models

class Village(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    tourism_status = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='villages/', null=True, blank=True)
    population = models.PositiveIntegerField(null=True, blank=True)
    language = models.CharField(max_length=100, blank=True)
    history = models.TextField(blank=True)
    featured = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Village"
        verbose_name_plural = "Villages"
        ordering = ['name']

    def __str__(self):
        return self.name

class Attraction(models.Model):
    ATTRACTION_TYPES = [
        ('natural', 'Natural'),
        ('cultural', 'Cultural'),
        ('historical', 'Historical'),
    ]

    name = models.CharField(max_length=255)
    village = models.ForeignKey(Village, on_delete=models.CASCADE, related_name='attractions')
    attraction_type = models.CharField(max_length=50, choices=ATTRACTION_TYPES)
    description = models.TextField()
    tourist_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = "Attraction"
        verbose_name_plural = "Attractions"
        ordering = ['name']

    def __str__(self):
        return self.name

class LocalSite(models.Model):
    SITE_TYPES = [
        ('museum', 'Museum'),
        ('monument', 'Monument'),
        ('park', 'Park'),
    ]

    name = models.CharField(max_length=255)
    village = models.ForeignKey(Village, on_delete=models.CASCADE, related_name='localsites')
    site_type = models.CharField(max_length=50, choices=SITE_TYPES)
    description = models.TextField()
    category = models.CharField(max_length=100, blank=True, null=True)  

    class Meta:
        verbose_name = "Local Site"
        verbose_name_plural = "Local Sites"
        ordering = ['name']

    def __str__(self):
        return self.name
