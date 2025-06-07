
from django.test import TestCase
from .models import Festival
from datetime import date

class FestivalModelTest(TestCase):

    def setUp(self):
        Festival.objects.create(
            name="Bamoun Cultural Festival",
            description="Celebration of Bamoun heritage and culture.",
            location="Foumban",
            start_date=date(2025, 8, 1),
            end_date=date(2025, 8, 5),
            is_featured=True
        )

    def test_festival_str(self):
        festival = Festival.objects.get(name="Bamoun Cultural Festival")
        self.assertEqual(str(festival), "Bamoun Cultural Festival")

    def test_festival_dates(self):
        festival = Festival.objects.get(name="Bamoun Cultural Festival")
        self.assertEqual(festival.start_date, date(2025, 8, 1))
        self.assertEqual(festival.end_date, date(2025, 8, 5))

    def test_festival_location(self):
        festival = Festival.objects.get(name="Bamoun Cultural Festival")
        self.assertEqual(festival.location, "Foumban")


