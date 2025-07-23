from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import Comment, Like, Share

class CommunityAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create(username='user')
        self.client.force_login(self.user)
    def test_comment_create(self):
        data = {'content_type': 'news', 'content_id': 1, 'content': '测试评论'}
        response = self.client.post('/comments/', data)
        self.assertIn(response.status_code, [200, 201])
    def test_like_create(self):
        data = {'target_type': 'news', 'target_id': 1, 'is_like': True}
        response = self.client.post('/likes/', data)
        self.assertIn(response.status_code, [200, 201])
    def test_share_create(self):
        data = {'content_type': 'news', 'content_id': 1, 'share_platform': 'wechat'}
        response = self.client.post('/shares/', data)
        self.assertIn(response.status_code, [200, 201])
    def test_report_create(self):
        data = {'target_type': 'comment', 'target_id': 1, 'reason': '不当言论'}
        response = self.client.post('/reports/', data)
        self.assertIn(response.status_code, [200, 201])
    def test_play_history_create(self):
        data = {'content_type': 'audio', 'content_id': 1, 'play_duration': 60, 'total_duration': 120}
        response = self.client.post('/play-history/', data)
        self.assertIn(response.status_code, [200, 201])
    def test_favorite_create(self):
        data = {'content_type': 'news', 'content_id': 1}
        response = self.client.post('/favorites/', data)
        self.assertIn(response.status_code, [200, 201])
    def test_user_behavior_stats_list(self):
        response = self.client.get('/user-behavior-stats/')
        self.assertIn(response.status_code, [200, 201, 204])
    def test_content_interaction_stats_list(self):
        response = self.client.get('/content-interaction-stats/')
        self.assertIn(response.status_code, [200, 201, 204])
    def test_user_profile_me(self):
        response = self.client.get('/user-profiles/me/')
        self.assertIn(response.status_code, [200, 201])
    def test_recommendation_personalized(self):
        response = self.client.get('/recommendations/personalized/')
        self.assertIn(response.status_code, [200, 201])
    def test_trending_topic_current(self):
        response = self.client.get('/trending-topics/current/')
        self.assertIn(response.status_code, [200, 201]) 