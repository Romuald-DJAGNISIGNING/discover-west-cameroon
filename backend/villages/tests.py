
from django.test import TestCase
from .models import Village, Attraction, LocalSite

class VillageModelTest(TestCase):

    def test_create_village(self):
        village = Village.objects.create(name="Buea", location="Southwest", population=200000, tourism_status=True)
        self.assertEqual(village.name, "Buea")
        self.assertTrue(village.tourism_status)

    def test_create_attraction(self):
        village = Village.objects.create(name="Buea", location="Southwest", population=200000, tourism_status=True)
        attraction = Attraction.objects.create(name="Mount Cameroon", village=village, attraction_type="natural", description="A volcanic mountain", tourist_rating=4.5)
        self.assertEqual(attraction.name, "Mount Cameroon")
        self.assertEqual(attraction.village, village)

    def test_create_local_site(self):
        village = Village.objects.create(name="Buea", location="Southwest", population=200000, tourism_status=True)
        local_site = LocalSite.objects.create(name="Buea Mountain Park", village=village, site_type="park", description="A beautiful park")
        self.assertEqual(local_site.name, "Buea Mountain Park")
        self.assertEqual(local_site.village, village)
