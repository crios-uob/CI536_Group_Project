from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
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
    .values("id", "question", "answer")
)

    return render(request, 'Flashcards.html', {
        'deck': deck,
        'cards': cards
    })  

def create_deck(request):

    # If user submitted the form
    if request.method == "POST":

        # Get form data from HTML inputs
        name = request.POST.get("name")
        category = request.POST.get("category")

        # Create new deck in database
        Deck.objects.create(
            name=name,
            category=category
        )

        # Redirect user back to decks page
        return redirect('decks')

    # If page is opened normally
    return render(request, 'create_deck.html')

def add_card(request, deck_id):

    # Get selected deck
    deck = get_object_or_404(Deck, id=deck_id)

    # If form submitted
    if request.method == "POST":

        # Get form data
        question = request.POST.get("question")
        answer = request.POST.get("answer")

        # Create card linked to deck
        Card.objects.create(
            deck=deck,
            question=question,
            answer=answer
        )

        # Redirect back to flashcards page
        return redirect('flashcards', deck_id=deck.id)

    # Load page normally
    return render(request, 'add_card.html', {
        'deck': deck
    })

def edit_card(request, card_id):

    # Get card object
    card = get_object_or_404(Card, id=card_id)

    # If form submitted
    if request.method == "POST":

        # Update card values
        card.question = request.POST.get("question")
        card.answer = request.POST.get("answer")

        # Save changes to database
        card.save()

        # Redirect back to flashcards page
        return redirect('flashcards', deck_id=card.deck.id)

    # Load page normally
    return render(request, 'edit_card.html', {
        'card': card
    })

def delete_card(request, card_id):

    # Get card object
    card = get_object_or_404(Card, id=card_id)

    # Save deck ID before deletion
    deck_id = card.deck.id

    # Delete card
    card.delete()

    # Redirect back to flashcards
    return redirect('flashcards', deck_id=deck_id)

def user_settings(request: HttpRequest) -> HttpResponse:
    """
    Loads the settings.html file and renders it with the Django template tags. 

    Args:
        request: Http Request Object

    Returns:
        HttpResponse Object with rendered HTML 
    """
    return render(request, 'settings.html', {})
