from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

class Deck(models.Model):
    name = models.CharField(max_length=100)
    category= models.CharField(max_length=50)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="decks",
        null=True,
        blank=True
    )

    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Card(models.Model):
    deck = models.ForeignKey(
        Deck, 
        on_delete=models.CASCADE,
        related_name='cards'
    )
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)

    def __str__(self):
        return self.question
    
class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    score = models.IntegerField()
    total = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.deck.name} - {self.score}"

class CardProgress(models.Model):
    WRONG = 1
    HARD = 2
    GOOD = 3
    EASY = 4

    LEARNING_NEW = 0
    LEARNING_ONE_MIN = 1
    LEARNING_TEN_MIN = 2
    GRADUATED = 3  

    learning_step = models.PositiveSmallIntegerField(default=LEARNING_NEW)

    RATINGS = [
        (WRONG, 'Wrong'),
        (HARD, 'Hard'),
        (GOOD, 'Good'),
        (EASY, 'Easy'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    card = models.ForeignKey(
        Card, 
        on_delete=models.CASCADE
    )

    ease_factor = models.FloatField(default=2.5)
    interval_days = models.PositiveIntegerField(default=0)
    repetitions = models.PositiveIntegerField(default=0)

    due_at = models.DateTimeField(default=timezone.now)
    last_reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user','card')

    def is_due(self) -> bool:
        return self.due_at <= timezone.now()