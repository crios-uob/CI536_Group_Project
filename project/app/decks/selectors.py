from django.utils import timezone
from models import CardProgress

def get_due_cards(user, deck=None):
    qs = CardProgress.objects.filter(
        user=user,
        due_at__lte=timezone.now()
    )

    if deck:
        qs = qs.filter(card__deck=deck)

    return qs.order_by("due_at")