from django.db import models
from django.utils.translation import gettext_lazy as _

class Festival(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"))
    location = models.CharField(_("Location"), max_length=255)
    start_date = models.DateField(_("Start Date"))
    end_date = models.DateField(_("End Date"))
    image = models.ImageField(_("Image"), upload_to='festival_images/', null=True, blank=True)
    is_featured = models.BooleanField(_("Is Featured"), default=False)

    class Meta:
        verbose_name = _("Festival")
        verbose_name_plural = _("Festivals")
        ordering = ['start_date']

    def __str__(self):
        return self.name

