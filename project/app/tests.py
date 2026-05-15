from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from app.views import analytics
from app.models import Deck, Card, Result

#user login tests
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

#Create models to test
class deckTestCase(TestCase):
    def deckTestCase(self):
        self.deck = Deck.objects.create(
            name="biology",
            category="science"
        )

    def test_deck_creation(self):
        self.assertEqual(
            self.deck.name,
            "biology"
        )

    def test_deck_string(self):
        self.assertEqual(
            str(self.deck),
            "science"
        )

    def test_name_max_length(self):
        max_length = self.deck._meta.get_field(
            'name'
        ).max_length

        self.assertEqual(max_length, 100)
    
    def test_category_max_length(self):
        max_length = self.deck._meta.get_field(
            'category'
        ).max_length

        self.assertEqual(max_length, 50)

class cardTestCase(TestCase):
    def cardTestCase(self):
        self.card = Card.objects.create(
            name="maths",
            category="subject"
        )

        self.card = Card.objects.create(
            question="1 + 1",
            answer="2",
            deck=self.deck
        )

    def test_card_creation(self):
        self.assertEqual(
            self.card.answer,
            "2"
        )

    def test_card_subject(self):
        self.assertEqual(
            self.card.deck.name,
            "maths"
        )

    def test_card_string(self):
        self.assertEqual(
            str(self.card),
            "1 + 1"
        )

class resultTestCase(TestCase):
    def resultTestCase(self):
        self.result = Result.objects.create(
            score=5,
            total=10
        )

    def test_result_creation(self):
        self.assertEqual(
            self.result.score,
            5
        )

        self.assertEqual(
            self.result.total,
            10
        )
    