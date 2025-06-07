from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Attraction(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='attractions/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='attractions')
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class LocalSite(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='local_sites/')
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.name

class TourPlan(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField()
    guide = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'guide'})
    attractions = models.ManyToManyField(Attraction, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.duration_days} days"
class TourActivity(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, related_name='activities')
    date = models.DateField()
    time = models.TimeField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.title} at {self.attraction.name} on {self.date}"
class TourReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.attraction.name}"

class TourCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class TourPhoto(models.Model):
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='tour_photos/')
    caption = models.CharField(max_length=255, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo of {self.attraction.name} by {self.uploaded_by.username if self.uploaded_by else 'Anonymous'}"
class TourGuide(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tour_guide_profile')
    bio = models.TextField(blank=True)
    expertise = models.CharField(max_length=255, blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"Guide: {self.user.username} - {self.expertise}"
class TourTransport(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='transport/')
    capacity = models.PositiveIntegerField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
class TourTransportBooking(models.Model):
    transport = models.ForeignKey(TourTransport, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.user.username} for {self.transport.name} on {self.date}"
class TourEvent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Event: {self.title} on {self.date}"
class TourEventRegistration(models.Model):
    event = models.ForeignKey(TourEvent, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} registered for {self.event.title} on {self.event.date}"
class TourFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, related_name='feedbacks')
    feedback_text = models.TextField()
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.username} for {self.attraction.name}"
class TourItinerary(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    attractions = models.ManyToManyField(Attraction, blank=True, related_name='itineraries')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Itinerary: {self.title} by {self.created_by.username if self.created_by else 'Anonymous'}"
class TourMap(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='tour_maps/')
    attractions = models.ManyToManyField(Attraction, blank=True, related_name='maps')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Map: {self.title} by {self.created_by.username if self.created_by else 'Anonymous'}"
class TourSafetyInfo(models.Model):
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, related_name='safety_info')
    safety_tips = models.TextField()
    emergency_contacts = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Safety Info for {self.attraction.name} by {self.created_by.username if self.created_by else 'Anonymous'}"

class TourWeatherInfo(models.Model):
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, related_name='weather_info')
    average_temperature = models.DecimalField(max_digits=5, decimal_places=2)
    best_visit_season = models.CharField(max_length=100, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Weather Info for {self.attraction.name} by {self.created_by.username if self.created_by else 'Anonymous'}"

class TourCulturalExperience(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, related_name='cultural_experiences')
    date = models.DateField()
    time = models.TimeField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='cultural_experiences/', blank=True, null=True)
    video = models.FileField(upload_to='cultural_experiences/videos/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    available_slots = models.PositiveIntegerField(default=0)
    booked_slots = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return f"Cultural Experience: {self.title} at {self.attraction.name} on {self.date} by {self.created_by.username if self.created_by else 'Anonymous'}"

class TourCulturalExperienceBooking(models.Model):
    experience = models.ForeignKey(TourCulturalExperience, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)
    number_of_slots = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Booking by {self.user.username} for {self.experience.title} on {self.experience.date}"
    def save(self, *args, **kwargs):
        if self.number_of_slots > self.experience.available_slots:
            raise ValueError("Not enough available slots for this booking.")
        self.experience.booked_slots += self.number_of_slots
        self.experience.available_slots -= self.number_of_slots
        self.experience.save()
        super().save(*args, **kwargs)
    def delete(self, *args, **kwargs):
        self.experience.available_slots += self.number_of_slots
        self.experience.booked_slots -= self.number_of_slots
        self.experience.save()
        super().delete(*args, **kwargs)
class TourCulturalExperienceReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    experience = models.ForeignKey(TourCulturalExperience, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.experience.title}"

    def save(self, *args, **kwargs):
        if self.rating < 1 or self.rating > 5:
            raise ValueError("Rating must be between 1 and 5.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        if self.experience.reviews.count() == 0:
            self.experience.delete()

    def get_average_rating(self):
        reviews = self.experience.reviews.all()
        if not reviews:
            return 0
        total_rating = sum(review.rating for review in reviews)
        return total_rating / reviews.count()

    def get_review_count(self):
        return self.experience.reviews.count()

    def get_user_reviews(self, user):
        return self.experience.reviews.filter(user=user)

    def get_experience_reviews(self):
        return self.experience.reviews.all()

    def get_experience_bookings(self):
        return self.experience.bookings.all()

    def get_experience_feedback(self):
        return self.experience.feedbacks.all()

    def get_experience_photos(self):
        return self.experience.photos.all()

    def get_experience_activities(self):
        return self.experience.activities.all()

    def get_experience_guides(self):
        return self.experience.guide_set.all()

    def get_experience_transport(self):
        return self.experience.transport_set.all()

    def get_experience_events(self):
        return self.experience.tourevent_set.all()

    def get_experience_itineraries(self):
        return self.experience.touritinerary_set.all()

    def get_experience_maps(self):
        return self.experience.tourmap_set.all()

    def get_experience_safety_info(self):
        return self.experience.safety_info.all()

    def get_experience_weather_info(self):
        return self.experience.weather_info.all()

    def get_experience_cultural_experiences(self):
        return self.experience.cultural_experiences.all()

    def get_experience_cultural_experience_bookings(self):
        return self.experience.cultural_experiencebooking_set.all()

    def get_experience_cultural_experience_reviews(self):
        return self.experience.cultural_experiencereview_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()

    def get_experience_cultural_experience_feedback(self):
        return self.experience.cultural_experiencefeedback_set.all()

    def get_experience_cultural_experience_photos(self):
        return self.experience.cultural_experiencephotos.all()

    def get_experience_cultural_experience_videos(self):
        return self.experience.cultural_experiencevideos.all()

    def get_experience_cultural_experience_guides(self):
        return self.experience.cultural_experienceguide_set.all()

    def get_experience_cultural_experience_transport(self):
        return self.experience.cultural_experiencetransport_set.all()

    def get_experience_cultural_experience_events(self):
        return self.experience.cultural_experienceevent_set.all()

    def get_experience_cultural_experience_itineraries(self):
        return self.experience.cultural_experienceitinerary_set.all()

    def get_experience_cultural_experience_maps(self):
        return self.experience.cultural_experiencemap_set.all()

    def get_experience_cultural_experience_safety_info(self):
        return self.experience.cultural_experiencesafetyinfo_set.all()

    def get_experience_cultural_experience_weather_info(self):
        return self.experience.cultural_experienceweatherinfo_set.all()