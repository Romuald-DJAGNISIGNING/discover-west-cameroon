from django.urls import reverse
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from .models import Village, VillageImage, VillageComment
from festivals.models import Festival
from PIL import Image
from io import BytesIO

User = get_user_model()

class VillageAppTests(APITestCase):
    def setUp(self):
        # Users
        self.tutor = User.objects.create_user(
            username='tutor',
            email='tutor@example.com',
            phone_number='+237600000003',
            password='pw',
            role='tutor'
        )
        self.guide = User.objects.create_user(
            username='guide',
            email='guide@example.com',
            phone_number='+237600000004',
            password='pw',
            role='guide'
        )
        self.learner = User.objects.create_user(
            username='learner',
            email='learner@example.com',
            phone_number='+237600000005',
            password='pw',
            role='learner'
        )
        self.visitor = User.objects.create_user(
            username='visitor',
            email='visitor@example.com',
            phone_number='+237600000006',
            password='pw',
            role='visitor'
        )

        # Village
        self.village = Village.objects.create(
            name="Bafoussam",
            description="Capital of the West Region.",
            department="Mifi",
            population=500000,
            tourism_status="high",
            latitude=5.47775,
            longitude=10.41759,
            main_languages="Ghomala, French",
            traditional_foods="Koki, Ndolé",
            cultural_highlights="Ngouon Festival",
            art_crafts="Bamileke masks",
            learn_more="Explore the Bamileke culture.",
            added_by=self.tutor,
        )

        # Linked Festival (for connection test)
        self.festival = Festival.objects.create(
            name="Ngouon",
            description="Bamoun Royal Festival",
            type="traditional",
            start_date="2025-12-05",
            end_date="2025-12-12",
            location="Foumban",
            village=self.village,
            main_language="Bamoun",
            is_annual=True,
            added_by=self.tutor,
        )

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def create_test_image(self):
        file = BytesIO()
        image = Image.new('RGB', (100, 100), color='red')
        image.save(file, 'jpeg')
        file.name = 'test.jpg'
        file.seek(0)
        return file

    def test_village_list_and_detail(self):
        url = reverse('village-list')
        response = self.client.get(url, HTTP_ACCEPT='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) > 0)
        detail_url = reverse('village-detail', args=[self.village.id])
        resp = self.client.get(detail_url, HTTP_ACCEPT='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['name'], "Bafoussam")

    def test_only_tutor_guide_can_create_village(self):
        url = reverse('village-list')
        data = {
            "name": "Baham",
            "description": "Another village.",
            "department": "Hauts-Plateaux",
            "population": 70000,
            "tourism_status": "medium",
            "latitude": 5.26667,
            "longitude": 10.46667,
            "main_languages": "Fe'fe', French",
            "added_by": self.tutor.id
        }
        self.authenticate(self.learner)
        response = self.client.post(url, data, format='json', HTTP_ACCEPT='application/json')
        self.assertEqual(response.status_code, 403)
        self.authenticate(self.tutor)
        response = self.client.post(url, data, format='json', HTTP_ACCEPT='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Village.objects.filter(name="Baham").exists())

    def test_update_and_delete_village(self):
        self.authenticate(self.tutor)
        url = reverse('village-detail', args=[self.village.id])
        response = self.client.patch(url, {"population": 600000}, format='json', HTTP_ACCEPT='application/json')
        self.assertEqual(response.status_code, 200)
        self.village.refresh_from_db()
        self.assertEqual(self.village.population, 600000)
        # Delete
        response = self.client.delete(url, HTTP_ACCEPT='application/json')
        self.assertEqual(response.status_code, 204)

    def test_village_image_upload_and_list(self):
        self.authenticate(self.tutor)
        url = reverse('villageimage-list')
        
        # Create a proper test image
        image_file = self.create_test_image()
        
        data = {
            "image": image_file,
            "caption": "Village View",
            "village": self.village.id
        }
        
        response = self.client.post(
            url, 
            data, 
            format='multipart',
            HTTP_ACCEPT='application/json'
        )
        
        self.assertEqual(response.status_code, 201, msg=response.data)
        self.assertEqual(VillageImage.objects.count(), 1)
        
        # List images
        response = self.client.get(url, HTTP_ACCEPT='application/json')
        self.assertEqual(response.status_code, 200)
        # Handle both list and non-list responses
        images_data = response.data if isinstance(response.data, list) else response.data.get('results', [])
        self.assertEqual(len(images_data), 1)
        self.assertEqual(images_data[0]['caption'], "Village View")

    def test_only_tutor_guide_can_upload_image(self):
        self.authenticate(self.learner)
        url = reverse('villageimage-list')
        image_file = self.create_test_image()
        data = {
            "image": image_file,
            "caption": "Learner Upload",
            "village": self.village.id
        }
        response = self.client.post(
            url, 
            data, 
            format='multipart',
            HTTP_ACCEPT='application/json'
        )
        self.assertEqual(response.status_code, 403)

    def test_village_comments_post_and_list(self):
        self.authenticate(self.learner)
        url = reverse('villagecomment-list')
        data = {
            "comment": "Nice place!",
            "user": self.learner.id,
            "village": self.village.id
        }
        response = self.client.post(url, data, format='json', HTTP_ACCEPT='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(VillageComment.objects.count(), 1)
        # List comments
        response = self.client.get(url, HTTP_ACCEPT='application/json')
        self.assertEqual(response.status_code, 200)
        # Handle both list and non-list responses
        comments_data = response.data if isinstance(response.data, list) else response.data.get('results', [])
        self.assertEqual(len(comments_data), 1)
        self.assertEqual(comments_data[0]['comment'], "Nice place!")

    def test_search_and_ordering(self):
        url = reverse('village-list')
        # Search by name
        response = self.client.get(url, {"search": "Bafoussam"}, HTTP_ACCEPT='application/json')
        self.assertEqual(response.status_code, 200)
        # Handle paginated and non-paginated responses
        results = response.data.get('results', []) if isinstance(response.data, dict) else response.data
        self.assertTrue(any(v['name'] == "Bafoussam" for v in results))
        # Ordering by population
        response = self.client.get(url, {"ordering": "-population"}, HTTP_ACCEPT='application/json')
        self.assertEqual(response.status_code, 200)

    def test_connect_village_to_festival(self):
        # Festival created in setUp with self.village
        self.assertEqual(self.festival.village, self.village)
        # If village is deleted, festival.village should become None
        self.authenticate(self.tutor)
        url = reverse('village-detail', args=[self.village.id])
        self.client.delete(url, HTTP_ACCEPT='application/json')
        self.festival.refresh_from_db()
        self.assertIsNone(self.festival.village)

    def test_map_utils(self):
        from villages.map_utils import openstreetmap_link, googlemaps_link
        lat, lon = float(self.village.latitude), float(self.village.longitude)
        osm_link = openstreetmap_link(lat, lon)
        gmaps_link = googlemaps_link(lat, lon)
        self.assertTrue("openstreetmap.org" in osm_link)
        self.assertTrue("maps.google.com" in gmaps_link)
        self.assertTrue(str(lat) in osm_link)
        self.assertTrue(str(lon) in gmaps_link)

    def test_village_map_html_renders(self):
        # Simulate map page rendering
        from django.test import RequestFactory
        from villages.views_map import village_map_view
        factory = RequestFactory()
        request = factory.get(f'/villages/{self.village.pk}/map/')
        response = village_map_view(request, pk=self.village.pk)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Bafoussam" in response.content)
        self.assertTrue(b"Leaflet" in response.content or b"tile.openstreetmap.org" in response.content)