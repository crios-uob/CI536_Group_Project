from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Deck, Card

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
