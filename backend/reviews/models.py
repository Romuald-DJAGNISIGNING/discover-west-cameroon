from django.db import models
from django.conf import settings
from villages.models import Village
from tourism.models import TouristicAttraction, HostingFamilyExperience, SocialImmersionExperience
from festivals.models import Festival

class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    # Generic link fields; only one should be set per review
    village = models.ForeignKey(Village, related_name="reviews", null=True, blank=True, on_delete=models.CASCADE)
    attraction = models.ForeignKey(TouristicAttraction, related_name="reviews", null=True, blank=True, on_delete=models.CASCADE)
    festival = models.ForeignKey(Festival, related_name="reviews", null=True, blank=True, on_delete=models.CASCADE)
    hosting_family = models.ForeignKey(HostingFamilyExperience, related_name="reviews", null=True, blank=True, on_delete=models.CASCADE)
    social_immersion = models.ForeignKey(SocialImmersionExperience, related_name="reviews", null=True, blank=True, on_delete=models.CASCADE)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (
            ("user", "village"),
            ("user", "attraction"),
            ("user", "festival"),
            ("user", "hosting_family"),
            ("user", "social_immersion"),
        )

    def __str__(self):
        target = self.village or self.attraction or self.festival or self.hosting_family or self.social_immersion
        return f"{self.user} review on {target}"