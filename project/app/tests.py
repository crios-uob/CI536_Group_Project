from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from app.views import analytics

#views.py tests
class userloginTestCase(TestCase):
    def login(self): #creates a test instance of model
        response = self.client.get('/analytics')
        self.assertEqual(response.status_code, 302) #checking if equal

    def useraccess(self):
        user = User.objects.create_user(
            username='testuser',
            password='password'
        )

        self.client.login(
            username='testuser',
            password='password123'
        )

        response = self.client.get('/analytics')
        self.assertEqual(response.status_code, 200)