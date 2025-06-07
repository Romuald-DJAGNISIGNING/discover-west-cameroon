from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

REVIEW_TARGET_CHOICES = [
    ('guide', 'Touristic Guide'),
    ('tutor', 'Tutor'),
    ('site', 'Tourist Site'),
    ('festival', 'Festival'),
    ('village', 'Village'),
]

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    target_type = models.CharField(max_length=50, choices=REVIEW_TARGET_CHOICES)
    target_id = models.PositiveIntegerField()
    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} rated {self.target_type} {self.target_id} ({self.rating}/5)"
