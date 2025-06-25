from django.db import models
from django.utils.translation import gettext_lazy as _


class Village(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    location = models.CharField(_("Location"), max_length=255)
    tourism_status = models.BooleanField(_("Tourism Status"), default=False)
    description = models.TextField(_("Description"), blank=True)
    photo = models.ImageField(_("Photo"), upload_to='villages/', null=True, blank=True)
    population = models.PositiveIntegerField(_("Population"), null=True, blank=True)
    language = models.CharField(_("Language"), max_length=100, blank=True)
    history = models.TextField(_("History"), blank=True)
    featured = models.BooleanField(_("Featured"), default=False)

    class Meta:
        verbose_name = _("Village")
        verbose_name_plural = _("Villages")
        ordering = ['name']

    def __str__(self):
        return self.name

class Attraction(models.Model):
    ATTRACTION_TYPES = [
        ('natural', _("Natural")),
        ('cultural', _("Cultural")),
        ('historical', _("Historical")),
    ]

    name = models.CharField(_("Name"), max_length=255)
    village = models.ForeignKey(Village, on_delete=models.CASCADE, related_name='attractions', verbose_name=_("Village"))
    attraction_type = models.CharField(_("Attraction Type"), max_length=50, choices=ATTRACTION_TYPES)
    description = models.TextField(_("Description"))
    tourist_rating = models.DecimalField(_("Tourist Rating"), max_digits=3, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = _("Attraction")
        verbose_name_plural = _("Attractions")
        ordering = ['name']

    def __str__(self):
        return self.name

class LocalSite(models.Model):
    SITE_TYPES = [
        ('museum', _("Museum")),
        ('monument', _("Monument")),
        ('park', _("Park")),
    ]

    name = models.CharField(_("Name"), max_length=255)
    village = models.ForeignKey(Village, on_delete=models.CASCADE, related_name='localsites', verbose_name=_("Village"))
    site_type = models.CharField(_("Site Type"), max_length=50, choices=SITE_TYPES)
    description = models.TextField(_("Description"))
    category = models.CharField(_("Category"), max_length=100, blank=True, null=True)  

    class Meta:
        verbose_name = _("Local Site")
        verbose_name_plural = _("Local Sites")
        ordering = ['name']

    def __str__(self):
        return self.name
