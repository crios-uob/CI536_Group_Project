from django.utils import timezone
from datetime import timedelta
from ..models import CardProgress

def review_card(progress: CardProgress, rating: int) -> CardProgress:
    """
    Spaced Repetition ALgo based off SM-2
    \nRatings:\n
      1 = Wrong
      2 = Hard 
      3 = Good 
      4 = Easy
    """

    now = timezone.now()
    minimum_clear_due_at = now + timedelta(days=1)

    def can_clear_deck() -> bool:
        return progress.due_at >= minimum_clear_due_at

    def update_learning_state():
        if can_clear_deck():
            progress.learning_step = CardProgress.GRADUATED
        elif progress.due_at <= now + timedelta(minutes=1):
            progress.learning_step = CardProgress.LEARNING_ONE_MIN
        else:
            progress.learning_step = CardProgress.LEARNING_TEN_MIN

    if rating == CardProgress.WRONG:
        progress.repetitions = 0
        progress.interval_days = 0
        progress.ease_factor = max(1.3, progress.ease_factor - 0.2)
        progress.due_at = now + timedelta(minutes=1)

    elif rating == CardProgress.HARD:
        progress.ease_factor = max(1.3, progress.ease_factor - 0.15)

        if progress.learning_step in [
            CardProgress.LEARNING_NEW,
            CardProgress.LEARNING_ONE_MIN,
        ]:
            progress.interval_days = 0
            progress.due_at = now + timedelta(minutes=10)

        elif progress.learning_step == CardProgress.LEARNING_TEN_MIN:
            progress.repetitions = max(1, progress.repetitions + 1)
            progress.interval_days = 1
            progress.due_at = now + timedelta(days=1)

        else:
            progress.repetitions += 1
            progress.interval_days = max(1, round(progress.interval_days))
            progress.due_at = now + timedelta(days=progress.interval_days)

    elif rating == CardProgress.GOOD:
        if progress.learning_step in [
            CardProgress.LEARNING_NEW,
            CardProgress.LEARNING_ONE_MIN,
        ]:
            progress.interval_days = 0
            progress.due_at = now + timedelta(minutes=10)

        elif progress.learning_step == CardProgress.LEARNING_TEN_MIN:
            progress.repetitions = 1
            progress.interval_days = 1
            progress.due_at = now + timedelta(days=1)

        else:
            progress.repetitions += 1

            if progress.interval_days <= 1:
                progress.interval_days = 2
            else:
                progress.interval_days = round(
                    progress.interval_days * progress.ease_factor
                )

            progress.due_at = now + timedelta(days=progress.interval_days)

    elif rating == CardProgress.EASY:
        progress.repetitions += 1
        progress.ease_factor += 0.15

        if progress.interval_days == 0:
            progress.interval_days = 1
        else:
            progress.interval_days = round(
                progress.interval_days * progress.ease_factor * 1.3
            )

        progress.due_at = now + timedelta(days=progress.interval_days)

    update_learning_state()

    progress.last_reviewed_at = now
    progress.save()

    return progress