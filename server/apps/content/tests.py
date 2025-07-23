from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import ContentTag

class ContentTagAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = get_user_model().objects.create(username='admin', is_staff=True)
        self.user = get_user_model().objects.create(username='user')
        self.tag = ContentTag.objects.create(name='科技')
    def test_tag_list(self):
        response = self.client.get('/content/tags')
        self.assertEqual(response.status_code, 200)
    def test_tag_create_no_permission(self):
        response = self.client.post('/content/tags', {'name': '娱乐'})
        self.assertEqual(response.status_code, 403)
    def test_tag_create_admin(self):
        self.client.force_login(self.admin)
        response = self.client.post('/content/tags', {'name': '娱乐'})
        self.assertEqual(response.status_code, 201)
    def test_batch_tag_relation(self):
        self.client.force_login(self.admin)
        # 假设有内容id=1，类型为rawnews
        ContentTag.objects.create(name='体育')
        data = {'content_type': 'rawnews', 'tags': ['科技', '体育']}
        response = self.client.post('/content/1/tags', data, content_type='application/json')
        self.assertIn(response.status_code, [200, 201])
    def test_tag_relation_permission(self):
        # 普通用户无权为非自己内容打标签
        data = {'content_type': 'rawnews', 'tags': ['科技']}
        response = self.client.post('/content/1/tags', data, content_type='application/json')
        self.assertEqual(response.status_code, 403)

class ContentModerationAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = get_user_model().objects.create(username='admin', is_staff=True)
    def test_moderation_post_no_permission(self):
        data = {'content_type': 'rawnews', 'status': 'approved'}
        response = self.client.post('/content/1/moderation', data, content_type='application/json')
        self.assertEqual(response.status_code, 403)
    def test_moderation_post_admin(self):
        self.client.force_login(self.admin)
        data = {'content_type': 'rawnews', 'status': 'approved'}
        response = self.client.post('/content/1/moderation', data, content_type='application/json')
        self.assertIn(response.status_code, [200, 201])

class ContentStatsAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create(username='user')
    def test_stats_auth_required(self):
        response = self.client.get('/content/1/stats?content_type=rawnews')
        self.assertEqual(response.status_code, 403)
    def test_stats_success(self):
        self.client.force_login(self.user)
        response = self.client.get('/content/1/stats?content_type=rawnews')
        self.assertIn(response.status_code, [200, 404]) 