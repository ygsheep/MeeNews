from django.test import TestCase, Client
from django.urls import reverse

class AITTSAPITest(TestCase):
    def setUp(self):
        self.client = Client()
    def test_tts_generate(self):
        response = self.client.post(reverse('ai/tts'))
        self.assertEqual(response.status_code, 201)
    def test_tts_status(self):
        response = self.client.get(reverse('ai/tts', kwargs={'task_id': 'tts_12345'}))
        self.assertEqual(response.status_code, 200) 