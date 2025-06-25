from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class Category(models.Model):
    name = models.CharField(_("Name"), max_length=100, unique=True)
    description = models.TextField(_("Description"), blank=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name

class Attraction(models.Model):
    name = models.CharField(_("Name"), max_length=200)
    description = models.TextField(_("Description"))
    location = models.CharField(_("Location"), max_length=255)
    image = models.ImageField(_("Image"), upload_to='attractions/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='attractions', verbose_name=_("Category"))
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Added By"))

    class Meta:
        verbose_name = _("Attraction")
        verbose_name_plural = _("Attractions")

    def __str__(self):
        return self.name

class LocalSite(models.Model):
    name = models.CharField(_("Name"), max_length=200)
    description = models.TextField(_("Description"))
    location = models.CharField(_("Location"), max_length=255)
    image = models.ImageField(_("Image"), upload_to='local_sites/')
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Added By"))
    category = models.CharField(_("Category"), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Local Site")
        verbose_name_plural = _("Local Sites")

    def __str__(self):
        return self.name

class TourPlan(models.Model):
    title = models.CharField(_("Title"), max_length=200)
    description = models.TextField(_("Description"))
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField(_("Duration (days)"))
    guide = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        limit_choices_to={'role': 'guide'}, verbose_name=_("Guide")
    )
    attractions = models.ManyToManyField(Attraction, blank=True, verbose_name=_("Attractions"))
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Tour Plan")
        verbose_name_plural = _("Tour Plans")

    def __str__(self):
        return f"{self.title} - {self.duration_days} days"

class TourActivity(models.Model):
    title = models.CharField(_("Title"), max_length=200)
    description = models.TextField(_("Description"))
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, related_name='activities', verbose_name=_("Attraction"))
    date = models.DateField(_("Date"))
    time = models.TimeField(_("Time"))
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Created By"))

    class Meta:
        verbose_name = _("Tour Activity")
        verbose_name_plural = _("Tour Activities")

    def __str__(self):
        return f"{self.title} at {self.attraction.name} on {self.date}"

class TourReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, related_name='reviews', verbose_name=_("Attraction"))
    rating = models.PositiveIntegerField(_("Rating"))
    comment = models.TextField(_("Comment"), blank=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Tour Review")
        verbose_name_plural = _("Tour Reviews")

    def __str__(self):
        return f"Review by {self.user.username} for {self.attraction.name}"

class TourCategory(models.Model):
    name = models.CharField(_("Name"), max_length=100, unique=True)
    description = models.TextField(_("Description"), blank=True)

    class Meta:
        verbose_name = _("Tour Category")
        verbose_name_plural = _("Tour Categories")

    def __str__(self):
        return self.name

class TourPhoto(models.Model):
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, related_name='photos', verbose_name=_("Attraction"))
    image = models.ImageField(_("Image"), upload_to='tour_photos/')
    caption = models.CharField(_("Caption"), max_length=255, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Uploaded By"))
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Tour Photo")
        verbose_name_plural = _("Tour Photos")

    def __str__(self):
        return f"Photo of {self.attraction.name} by {self.uploaded_by.username if self.uploaded_by else 'Anonymous'}"

class TourGuide(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tour_guide_profile', verbose_name=_("User"))
    bio = models.TextField(_("Bio"), blank=True)
    expertise = models.CharField(_("Expertise"), max_length=255, blank=True)
    available = models.BooleanField(_("Available"), default=True)

    class Meta:
        verbose_name = _("Tour Guide")
        verbose_name_plural = _("Tour Guides")

    def __str__(self):
        return f"Guide: {self.user.username} - {self.expertise}"

class TourTransport(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    description = models.TextField(_("Description"), blank=True)
    image = models.ImageField(_("Image"), upload_to='transport/')
    capacity = models.PositiveIntegerField(_("Capacity"))
    available = models.BooleanField(_("Available"), default=True)

    class Meta:
        verbose_name = _("Tour Transport")
        verbose_name_plural = _("Tour Transports")

    def __str__(self):
        return self.name

class TourTransportBooking(models.Model):
    transport = models.ForeignKey(TourTransport, on_delete=models.CASCADE, related_name='bookings', verbose_name=_("Transport"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    date = models.DateField(_("Date"))
    time = models.TimeField(_("Time"))
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Tour Transport Booking")
        verbose_name_plural = _("Tour Transport Bookings")

    def __str__(self):
        return f"Booking by {self.user.username} for {self.transport.name} on {self.date}"

class TourEvent(models.Model):
    title = models.CharField(_("Title"), max_length=200)
    description = models.TextField(_("Description"))
    date = models.DateField(_("Date"))
    time = models.TimeField(_("Time"))
    location = models.CharField(_("Location"), max_length=255)
    image = models.ImageField(_("Image"), upload_to='events/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Created By"))

    class Meta:
        verbose_name = _("Tour Event")
        verbose_name_plural = _("Tour Events")

    def __str__(self):
        return f"Event: {self.title} on {self.date}"

class TourEventRegistration(models.Model):
    event = models.ForeignKey(TourEvent, on_delete=models.CASCADE, related_name='registrations', verbose_name=_("Event"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    registered_at = models.DateTimeField(_("Registered At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Tour Event Registration")
        verbose_name_plural = _("Tour Event Registrations")

    def __str__(self):
        return f"{self.user.username} registered for {self.event.title} on {self.event.date}"

class TourFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, related_name='feedbacks', verbose_name=_("Attraction"))
    feedback_text = models.TextField(_("Feedback Text"))
    rating = models.PositiveIntegerField(_("Rating"))
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Tour Feedback")
        verbose_name_plural = _("Tour Feedbacks")

    def __str__(self):
        return f"Feedback by {self.user.username} for {self.attraction.name}"

class TourItinerary(models.Model):
    title = models.CharField(_("Title"), max_length=200)
    description = models.TextField(_("Description"))
    attractions = models.ManyToManyField(Attraction, blank=True, related_name='itineraries', verbose_name=_("Attractions"))
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Created By"))
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Tour Itinerary")
        verbose_name_plural = _("Tour Itineraries")

    def __str__(self):
        return f"Itinerary: {self.title} by {self.created_by.username if self.created_by else 'Anonymous'}"

class TourMap(models.Model):
    title = models.CharField(_("Title"), max_length=200)
    description = models.TextField(_("Description"), blank=True)
    image = models.ImageField(_("Image"), upload_to='tour_maps/')
    attractions = models.ManyToManyField(Attraction, blank=True, related_name='maps', verbose_name=_("Attractions"))
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Created By"))
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Tour Map")
        verbose_name_plural = _("Tour Maps")

    def __str__(self):
        return f"Map: {self.title} by {self.created_by.username if self.created_by else 'Anonymous'}"

class TourSafetyInfo(models.Model):
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, related_name='safety_info', verbose_name=_("Attraction"))
    safety_tips = models.TextField(_("Safety Tips"))
    emergency_contacts = models.TextField(_("Emergency Contacts"), blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Created By"))
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Tour Safety Info")
        verbose_name_plural = _("Tour Safety Infos")

    def __str__(self):
        return f"Safety Info for {self.attraction.name} by {self.created_by.username if self.created_by else 'Anonymous'}"

class TourWeatherInfo(models.Model):
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, related_name='weather_info', verbose_name=_("Attraction"))
    average_temperature = models.DecimalField(_("Average Temperature"), max_digits=5, decimal_places=2)
    best_visit_season = models.CharField(_("Best Visit Season"), max_length=100, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Created By"))
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Tour Weather Info")
        verbose_name_plural = _("Tour Weather Infos")

    def __str__(self):
        return f"Weather Info for {self.attraction.name} by {self.created_by.username if self.created_by else 'Anonymous'}"

class TourCulturalExperience(models.Model):
    title = models.CharField(_("Title"), max_length=200)
    description = models.TextField(_("Description"))
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, related_name='cultural_experiences', verbose_name=_("Attraction"))
    date = models.DateField(_("Date"))
    time = models.TimeField(_("Time"))
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Created By"))
    image = models.ImageField(_("Image"), upload_to='cultural_experiences/', blank=True, null=True)
    video = models.FileField(_("Video"), upload_to='cultural_experiences/videos/', blank=True, null=True)
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2, default=0.00)
    available_slots = models.PositiveIntegerField(_("Available Slots"), default=0)
    booked_slots = models.PositiveIntegerField(_("Booked Slots"), default=0)
    is_active = models.BooleanField(_("Is Active"), default=True)

    class Meta:
        verbose_name = _("Tour Cultural Experience")
        verbose_name_plural = _("Tour Cultural Experiences")

    def __str__(self):
        return f"Cultural Experience: {self.title} at {self.attraction.name} on {self.date} by {self.created_by.username if self.created_by else 'Anonymous'}"

class TourCulturalExperienceBooking(models.Model):
    experience = models.ForeignKey(TourCulturalExperience, on_delete=models.CASCADE, related_name='bookings', verbose_name=_("Experience"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    booked_at = models.DateTimeField(_("Booked At"), auto_now_add=True)
    number_of_slots = models.PositiveIntegerField(_("Number of Slots"), default=1)

    class Meta:
        verbose_name = _("Tour Cultural Experience Booking")
        verbose_name_plural = _("Tour Cultural Experience Bookings")

    def __str__(self):
        return f"Booking by {self.user.username} for {self.experience.title} on {self.experience.date}"

    def save(self, *args, **kwargs):
        if self.number_of_slots > self.experience.available_slots:
            raise ValueError(_("Not enough available slots for this booking."))
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    experience = models.ForeignKey(TourCulturalExperience, on_delete=models.CASCADE, related_name='reviews', verbose_name=_("Experience"))
    rating = models.PositiveIntegerField(_("Rating"))
    comment = models.TextField(_("Comment"), blank=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Tour Cultural Experience Review")
        verbose_name_plural = _("Tour Cultural Experience Reviews")

    def __str__(self):
        return f"Review by {self.user.username} for {self.experience.title}"

    def save(self, *args, **kwargs):
        if self.rating < 1 or self.rating > 5:
            raise ValueError(_("Rating must be between 1 and 5."))
        super().save(*args, **kwargs)