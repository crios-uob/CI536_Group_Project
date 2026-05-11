from django.utils import timezone
from datetime import timedelta
from models import CardProgress

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
    if rating == CardProgress.WRONG:
        progress.repetitions = 0
        progress.interval_days = 0
        progress.ease_factor = max(1.3, progress.ease_factor - 0.2)
        progress.due_at = now + timedelta(minutes=10)
    elif rating == CardProgress.HARD:
        progress.repetitions += 1
        progress.ease_factor = max(1.3, progress.ease_factor - 0.15)

        if progress.interval_days == 0:
            progress.interval_days = 1
        else:
            progress.interval_days = max(1, round(progress.interval_days))

        progress.due_at = now + timedelta(days=progress.interval_days)

    elif rating == CardProgress.GOOD:
        progress.repetitions += 1

        if progress.interval_days == 1:
            progress.interval_days = 1
        elif progress.interval_days == 2:
            progress.interval_days = 3
        else:
            progress.interval_days = round(
                progress.interval_days * progress.ease_factor
            )

        progress.due_at = now + timedelta(days=progress.interval_days)

    elif rating == CardProgress.EASY:
        progress.repetitions += 1
        progress.ease_factor += 0.15

        if progress.interval_days == 0:
            progress.interval_days = 4
        else:
            progress.interval_days = round(
                progress.interval_days * progress.ease_factor * 1.3
            )

        progress.due_at = now + timedelta(days=progress.interval_days)

    progress.last_reviewed_at = now
    progress.save()

    return progress
