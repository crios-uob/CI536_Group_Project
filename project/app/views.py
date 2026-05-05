from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json
from .models import Result, Deck, Card

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

def analytics(request: HttpRequest) -> HttpResponse:
    """
    Loads the analytics.html file and renders it with the Django template tags. 

    Args:
        request: Http Request Object

    Returns:
        HttpResponse Object with rendered HTML 
    """
    return render(request, 'analytics.html', {})

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

def quiz(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)
    cards = Card.objects.filter(deck=deck)

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
    cards = Card.objects.filter(deck=deck)

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
