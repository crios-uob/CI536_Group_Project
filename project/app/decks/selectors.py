from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from ..models import CardProgress

def get_due_cards(user, deck=None):
    now = timezone.now()

    due_card_progress = CardProgress.objects.filter(
        user=user,
        due_at__lt = now + timedelta(days=1)
    )

    if deck:
        due_card_progress = due_card_progress.filter(card__deck=deck)

    return due_card_progress.order_by("due_at")