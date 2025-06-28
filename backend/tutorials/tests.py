from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from villages.models import Village
from tourism.models import TouristicAttraction
from festivals.models import Festival
from .models import Tutorial, TutorialCategory, TutorialComment
from rest_framework import status

User = get_user_model()

class TutorialsAppTests(APITestCase):
    def setUp(self):
        # Create test users
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            phone_number='+237600000001',
            password='adminpw'
        )
        self.tutor = User.objects.create_user(
            username='tutor',
            email='tutor@example.com',
            phone_number='+237600000007',
            password='pw',
            role='tutor'
        )
        self.guide = User.objects.create_user(
            username='guide',
            email='guide@example.com',
            phone_number='+237600000009',
            password='pw',
            role='guide'
        )
        self.learner = User.objects.create_user(
            username='learner',
            email='learner@example.com',
            phone_number='+237600000008',
            password='pw',
            role='learner'
        )
        
        # Create test category
        self.cat = TutorialCategory.objects.create(
            name="Culture", 
            description="Culture-related tutorials"
        )
        
        # Create test village
        self.village = Village.objects.create(
            name="Bamenda", 
            department="Mezam", 
            description="Bamenda desc", 
            population=500000
        )
        
        # Create test attraction
        self.attraction = TouristicAttraction.objects.create(
            name="Bamenda Waterfall", 
            description="Waterfall desc", 
            village=self.village, 
            added_by=self.tutor
        )
        
        # Create test festival
        self.festival = Festival.objects.create(
            name="Bamenda Fest", 
            description="Fest desc", 
            type="cultural",
            start_date="2025-10-10", 
            end_date="2025-10-12", 
            location="Bamenda", 
            village=self.village, 
            main_language="Meta", 
            is_annual=True, 
            added_by=self.tutor
        )
        
        # Create published tutorial
        self.tut = Tutorial.objects.create(
            title="How to Participate in Bamenda Fest",
            category=self.cat,
            description="A guide",
            content="Step 1: ...",
            village=self.village,
            attraction=self.attraction,
            festival=self.festival,
            created_by=self.tutor,
            is_published=True
        )
        
        # Create unpublished tutorial
        self.unpublished_tut = Tutorial.objects.create(
            title="Unpublished Tutorial",
            category=self.cat,
            description="Not published",
            content="Hidden content",
            created_by=self.tutor,
            is_published=False
        )
        
        # Create test comment
        self.comment = TutorialComment.objects.create(
            tutorial=self.tut,
            user=self.learner,
            comment="Test comment"
        )

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    # =============== Tutorial Listing Tests ===============
    def test_list_tutorials_unauthenticated(self):
        url = reverse('tutorials:tutorial-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        results = resp.data.get('results', resp.data)
        published_titles = [t['title'] for t in results]
        self.assertIn(self.tut.title, published_titles)
        self.assertNotIn(self.unpublished_tut.title, published_titles)

    def test_list_tutorials_authenticated(self):
        self.authenticate(self.learner)
        url = reverse('tutorials:tutorial-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        results = resp.data.get('results', resp.data)
        published_titles = [t['title'] for t in results]
        self.assertIn(self.tut.title, published_titles)
        self.assertNotIn(self.unpublished_tut.title, published_titles)

    def test_admin_can_see_unpublished_tutorials(self):
        self.authenticate(self.admin)
        url = reverse('tutorials:tutorial-list')
        resp = self.client.get(url, {'show_all': 'true'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        results = resp.data.get('results', resp.data)
        all_titles = [t['title'] for t in results]
        self.assertIn(self.tut.title, all_titles)
        self.assertIn(self.unpublished_tut.title, all_titles)

    # =============== Tutorial Creation Tests ===============
    def test_tutor_can_create_tutorial(self):
        self.authenticate(self.tutor)
        url = reverse('tutorials:tutorial-list')
        data = {
            "title": "Festival Cooking",
            "category": self.cat.id,
            "description": "Cooking details",
            "content": "How to cook...",
            "village": self.village.id,
            "is_published": True,
        }
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Tutorial.objects.filter(title="Festival Cooking").exists())

    def test_guide_can_create_tutorial(self):
        self.authenticate(self.guide)
        url = reverse('tutorials:tutorial-list')
        data = {
            "title": "Guide Tutorial",
            "category": self.cat.id,
            "content": "Guide content",
            "is_published": True,
        }
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_learner_cannot_create_tutorial(self):
        self.authenticate(self.learner)
        url = reverse('tutorials:tutorial-list')
        data = {"title": "Not allowed", "category": self.cat.id, "content": "Test"}
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    # =============== Tutorial Detail Tests ===============
    def test_tutorial_detail_view(self):
        url = reverse('tutorials:tutorial-detail', args=[self.tut.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['title'], self.tut.title)
        self.assertEqual(len(resp.data['comments']), 1)

    def test_unpublished_tutorial_not_visible(self):
        url = reverse('tutorials:tutorial-detail', args=[self.unpublished_tut.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_can_view_unpublished_tutorial(self):
        self.authenticate(self.admin)
        url = reverse('tutorials:tutorial-detail', args=[self.unpublished_tut.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['title'], self.unpublished_tut.title)

    # =============== Tutorial Update Tests ===============
    def test_owner_can_update_tutorial(self):
        self.authenticate(self.tutor)
        url = reverse('tutorials:tutorial-detail', args=[self.tut.id])
        data = {"title": "Updated Title"}
        resp = self.client.patch(url, data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.tut.refresh_from_db()
        self.assertEqual(self.tut.title, "Updated Title")

    def test_non_owner_cannot_update_tutorial(self):
        tutor_tut = Tutorial.objects.create(
            title="Owned by tutor",
            category=self.cat,
            content="Content",
            created_by=self.tutor,
            is_published=True
        )
        
        self.authenticate(self.guide)
        url = reverse('tutorials:tutorial-detail', args=[tutor_tut.id])
        data = {"title": "Unauthorized Update"}
        resp = self.client.patch(url, data)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_update_any_tutorial(self):
        self.authenticate(self.admin)
        url = reverse('tutorials:tutorial-detail', args=[self.tut.id])
        data = {"title": "Admin Updated Title"}
        resp = self.client.patch(url, data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    # =============== Tutorial Deletion Tests ===============
    def test_owner_can_delete_tutorial(self):
        self.authenticate(self.tutor)
        url = reverse('tutorials:tutorial-detail', args=[self.tut.id])
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Tutorial.objects.filter(id=self.tut.id).exists())

    def test_admin_can_delete_any_tutorial(self):
        self.authenticate(self.admin)
        url = reverse('tutorials:tutorial-detail', args=[self.tut.id])
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_non_owner_cannot_delete_tutorial(self):
        tutor_tut = Tutorial.objects.create(
            title="Owned by tutor",
            category=self.cat,
            content="Content",
            created_by=self.tutor,
            is_published=True
        )
        
        self.authenticate(self.guide)
        url = reverse('tutorials:tutorial-detail', args=[tutor_tut.id])
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    # =============== Comment Tests ===============
    def test_add_comment(self):
        self.authenticate(self.learner)
        url = reverse('tutorials:tutorial-add-comment', args=[self.tut.id])
        data = {"comment": "Great tutorial!"}
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TutorialComment.objects.count(), 2)

    def test_add_empty_comment(self):
        self.authenticate(self.learner)
        url = reverse('tutorials:tutorial-add-comment', args=[self.tut.id])
        data = {"comment": ""}
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_comments(self):
        self.authenticate(self.learner)
        url = reverse('tutorials:tutorialcomment-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        results = resp.data.get('results', resp.data)
        self.assertTrue(any(c['comment'] == "Test comment" for c in results))

    def test_delete_comment_as_owner(self):
        self.authenticate(self.learner)
        url = reverse('tutorials:tutorialcomment-detail', args=[self.comment.id])
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(TutorialComment.objects.filter(id=self.comment.id).exists())

    def test_cannot_delete_others_comments(self):
        tutor_comment = TutorialComment.objects.create(
            tutorial=self.tut,
            user=self.tutor,
            comment="Tutor's comment"
        )
        
        self.authenticate(self.learner)
        url = reverse('tutorials:tutorialcomment-detail', args=[tutor_comment.id])
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(TutorialComment.objects.filter(id=tutor_comment.id).exists())

    # =============== Filtering Tests ===============
    def test_filter_tutorials_by_category(self):
        url = reverse('tutorials:tutorial-list')
        resp = self.client.get(url, {'category': self.cat.id})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        
        data = resp.data
        results = data['results'] if 'results' in data else data
        
        if results:
            self.assertEqual(results[0]['category'], self.cat.id)

    def test_filter_tutorials_by_village(self):
        url = reverse('tutorials:tutorial-list')
        resp = self.client.get(url, {'village': self.village.id})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        results = resp.data.get('results', resp.data)
        if results:
            self.assertEqual(results[0]['village'], self.village.id)

    def test_filter_tutorials_by_attraction(self):
        url = reverse('tutorials:tutorial-list')
        resp = self.client.get(url, {'attraction': self.attraction.id})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        results = resp.data.get('results', resp.data)
        if results:
            self.assertEqual(results[0]['attraction'], self.attraction.id)

    def test_pagination(self):
        for i in range(15):
            Tutorial.objects.create(
                title=f"Test Tutorial {i}",
                category=self.cat,
                content="Content",
                created_by=self.tutor,
                is_published=True
            )
        
        url = reverse('tutorials:tutorial-list')
        resp = self.client.get(url, {'page': 2})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('count', resp.data)
        self.assertIn('results', resp.data)

    def test_invalid_comment(self):
        self.authenticate(self.learner)
        url = reverse('tutorials:tutorial-add-comment', args=[self.tut.id])
        resp = self.client.post(url, {"comment": ""}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('comment', resp.data)

    def test_tutor_cannot_modify_others_tutorials(self):
        tutor2 = User.objects.create_user(
            username='tutor2',
            email='tutor2@example.com',
            phone_number='+237600000002',
            password='pw',
            role='tutor'
        )

        self.authenticate(tutor2)
        
        url = reverse('tutorials:tutorial-detail', args=[self.tut.id])
        resp = self.client.patch(url, {"title": "Unauthorized Edit"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_bypasses_ownership(self):
        self.authenticate(self.admin)
        url = reverse('tutorials:tutorial-detail', args=[self.tut.id])
        resp = self.client.patch(url, {"title": "Admin Override"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.tut.refresh_from_db()
        self.assertEqual(self.tut.title, "Admin Override")

    def test_guide_can_create_but_not_modify_others(self):
        guide2 = User.objects.create_user(
            username='guide2',
            email='guide2@example.com',
            phone_number='+237600000003',
            password='pw',
            role='guide'
        )
        self.authenticate(guide2)
        
        create_url = reverse('tutorials:tutorial-list')
        create_resp = self.client.post(create_url, {
            "title": "New Guide Tutorial",
            "category": self.cat.id,
            "content": "Content"
        })
        self.assertEqual(create_resp.status_code, status.HTTP_201_CREATED)
        
        update_url = reverse('tutorials:tutorial-detail', args=[self.tut.id])
        update_resp = self.client.patch(update_url, {"title": "Unauthorized"})
        self.assertEqual(update_resp.status_code, status.HTTP_403_FORBIDDEN)