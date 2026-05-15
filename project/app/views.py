from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models.functions import TruncDate
from django.db.models import Avg
import json
from .models import Result, Deck, Card, CardAttempt

# Create your views here.

def test(request: HttpRequest) -> HttpResponse:
    """
    Loads the test.html file and renders it with the Django template tags. 

    Args:
        request: Http Request Object

    Returns:
        HttpResponse Object with rendered HTML 
    """
    return render(request, 'test.html', {'name': 'Jason'})

@login_required
def analytics(request: HttpRequest) -> HttpResponse:
    results = Result.objects.filter(user=request.user)

    total_quizzes = results.count()
    #For accuracy % calcs
    total_correct = sum(result.score for result in results)
    total_questions = sum(result.total for result in results)
    accuracy = 0 #default

    if total_questions > 0:
        accuracy = round((total_correct / total_questions) * 100, 2) #accuracy % to 2 d.p.

    #Data for graphs
    #For score history
    daily_results = (
        results
        .annotate(day=TruncDate("date_taken")) #date only, time not required
        .values("day")
        .annotate(avg_score=Avg("score")) #average score by date
        .order_by("day") #ascending order
    )

    labels = [] #list for dates
    scores = [] #list for avg scores

    #Assigning to lists
    for entry in daily_results:
        labels.append(str(entry["day"])) #into string
        scores.append(round(entry["avg_score"], 2)) 

    context = { 
        "total_quizzes": total_quizzes,
        "total_correct": total_correct,
        "total_questions": total_questions,
        "accuracy": accuracy,
        "labels": labels,
        "scores": scores,
    }

    return render(request, 'analytics.html', context)

def save_result(request):
    if request.method == "POST":
        data = json.loads(request.body)

        score = data.get("score")
        total = data.get("total")
        deck_id = data.get("deck_id")

        deck = Deck.objects.get(id=deck_id)

        Result.objects.create(
            user=request.user,
            deck=deck,
            score=score,
            total=total
        )

        return JsonResponse({"status": "success"})

def quiz_mc(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)
    cards = list(
    Card.objects.filter(deck=deck)
    .values("question", "answer")
)

    return render(request, 'quiz_mc.html', {
        'deck': deck,
        'cards': cards
    })

def quiz(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)
    cards = list(
    Card.objects.filter(deck=deck)
    .values("question", "answer")
)

    return render(request, 'quiz.html', {
        'deck': deck,
        'cards': cards
    })

def decks(request):
    all_decks = Deck.objects.all()
    return render(request, 'decks.html', {'decks': all_decks})

from .models import Deck

def file(request):
    decks = Deck.objects.all()
    return render(request, 'file.html', {'decks': decks})

def flashcards(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)
    cards = list(
    Card.objects.filter(deck=deck)
    .values("question", "answer")
)

    return render(request, 'Flashcards.html', {
        'deck': deck,
        'cards': cards
    })  

def user_settings(request: HttpRequest) -> HttpResponse:
    """
    Loads the settings.html file and renders it with the Django template tags. 

    Args:
        request: Http Request Object

    Returns:
        HttpResponse Object with rendered HTML 
    """
    return render(request, 'settings.html', {})
