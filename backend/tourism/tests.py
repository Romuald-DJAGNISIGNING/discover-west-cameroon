# tourism/tests.py

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import CustomUser
from .models import Category, Attraction, LocalSite, TourPlan

class TourismAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            email="testuser@gmail.com",
            username="testuser",
            phone_number="+237612345678",
            full_name="Test User",
            password="testpass123"
        )
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(name="Historical", description="Historical places")
        self.attraction = Attraction.objects.create(
            name="Mount Cameroon", 
            description="Highest peak in West Africa", 
            location="Buea", 
            image="test.jpg",
            category=self.category
        )
        self.site = LocalSite.objects.create(
            name="Fon's Palace",
            description="Traditional palace in Bamenda",
            location="Bamenda",
            image="palace.jpg",
            category=self.category
        )
        self.tour_plan = TourPlan.objects.create(
            title="2 Days Mount Cameroon Hike",
            description="Experience hiking the tallest mountain",
            price=50000,
            duration="2 days",
            guide=self.user
        )

    def test_list_categories(self):
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_category(self):
        data = {"name": "Cultural", "description": "Cultural heritage"}
        response = self.client.post(reverse('category-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_attractions(self):
        response = self.client.get(reverse('attraction-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_local_sites(self):
        response = self.client.get(reverse('localsite-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_tour_plans(self):
        response = self.client.get(reverse('tourplan-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_tour_plan(self):
        data = {
            "title": "3 Days Cultural Tour",
            "description": "Explore cultural sites in West Cameroon",
            "price": 75000,
            "duration_days": 3,
            "guide": self.user.id,
            "attraction_ids": [self.attraction.id, self.site.id]
        }
        response = self.client.post(reverse('tourplan-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TourPlan.objects.count(), 2)

    def test_tour_plan_detail(self):
        response = self.client.get(reverse('tourplan-detail', kwargs={'pk': self.tour_plan.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.tour_plan.title)

    def test_update_tour_plan(self):
        data = {
            "title": "Updated Tour Plan",
            "description": "Updated description",
            "price": 60000,
            "duration_days": 2,
            "guide": self.user.id,
            "attraction_ids": [self.attraction.id]
        }
        response = self.client.put(reverse('tourplan-detail', kwargs={'pk': self.tour_plan.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tour_plan.refresh_from_db()
        self.assertEqual(self.tour_plan.title, "Updated Tour Plan")

    def test_delete_tour_plan(self):
        response = self.client.delete(reverse('tourplan-detail', kwargs={'pk': self.tour_plan.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TourPlan.objects.count(), 0)

    def test_create_attraction_with_category(self):
        data = {
            "name": "Limbe Botanic Garden",
            "description": "A beautiful garden in Limbe",
            "location": "Limbe",
            "image": "garden.jpg",
            "category_id": self.category.id
        }
        response = self.client.post(reverse('attraction-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Attraction.objects.count(), 2)
        self.assertEqual(Attraction.objects.last().name, "Limbe Botanic Garden")

    def test_create_local_site(self):
        data = {
            "name": "Bamenda Grand Mall",
            "description": "Shopping mall in Bamenda",
            "location": "Bamenda",
            "image": "mall.jpg",
            "category_id": self.category.id
        }
        response = self.client.post(reverse('localsite-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LocalSite.objects.count(), 2)
        self.assertEqual(LocalSite.objects.last().name, "Bamenda Grand Mall")

    def test_category_detail(self):
        response = self.client.get(reverse('category-detail', kwargs={'pk': self.category.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.category.name)
        self.assertEqual(response.data['description'], self.category.description)

    def test_update_category(self):
        data = {
            "name": "Updated Historical",
            "description": "Updated description for historical places"
        }
        response = self.client.put(reverse('category-detail', kwargs={'pk': self.category.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, "Updated Historical")
        self.assertEqual(self.category.description, "Updated description for historical places")

    def test_delete_category(self):
        response = self.client.delete(reverse('category-detail', kwargs={'pk': self.category.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)

    def test_create_tour_plan_without_guide(self):
        data = {
            "title": "Solo Tour Plan",
            "description": "A tour plan without a guide",
            "price": 30000,
            "duration_days": 1,
            "attraction_ids": [self.attraction.id]
        }
        response = self.client.post(reverse('tourplan-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TourPlan.objects.count(), 2)
        self.assertIsNone(TourPlan.objects.last().guide)

    def test_create_tour_plan_with_invalid_attraction(self):
        data = {
            "title": "Invalid Tour Plan",
            "description": "Tour plan with non-existent attraction",
            "price": 40000,
            "duration_days": 2,
            "guide": self.user.id,
            "attraction_ids": [9999]  # Non-existent attraction ID
        }
        response = self.client.post(reverse('tourplan-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(TourPlan.objects.count(), 1)

    def test_create_attraction_without_category(self):
        data = {
            "name": "New Attraction",
            "description": "An attraction without a category",
            "location": "Yaoundé",
            "image": "attraction.jpg"
        }
        response = self.client.post(reverse('attraction-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Attraction.objects.count(), 1)

    def test_create_local_site_without_category(self):
        data = {
            "name": "New Local Site",
            "description": "A local site without a category",
            "location": "Douala",
            "image": "localsite.jpg"
        }
        response = self.client.post(reverse('localsite-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(LocalSite.objects.count(), 1)  

    def test_list_tour_plans_with_filter(self):
        response = self.client.get(reverse('tourplan-list'), {'guide': self.user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.tour_plan.title)

    def test_list_attractions_by_category(self):
        response = self.client.get(reverse('attraction-list'), {'category': self.category.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.attraction.name)

    def test_list_local_sites_by_category(self):
        response = self.client.get(reverse('localsite-list'), {'category': self.category.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.site.name)

    def test_tour_plan_with_attractions(self):
        response = self.client.get(reverse('tourplan-detail', kwargs={'pk': self.tour_plan.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('attractions', response.data)
        self.assertEqual(len(response.data['attractions']), 0)
