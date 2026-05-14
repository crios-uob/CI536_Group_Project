from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
import json
from .models import Result, Deck, Card, CardProgress
from .decks.services import review_card
from .decks.selectors import get_due_cards
from .decks.forms import DeckForm

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

def dashboard(request: HttpRequest) -> HttpResponse:
    """
    Loads the dashboard.html file and renders it with the Django template tags. 
    
    Returns:
        HttpResponse Object with rendered HTML 
    """
    return render(request, 'dashboard.html', {})

def about(request):
    return render(request, 'about.html')

# Save quiz result asychronously from JavaScript fetch request
def save_result(request):
    # Only allow POST requests
    if request.method == "POST":
        # Convert incoming JSON data to Python dictionary
        data = json.loads(request.body)

        # Extract quiz data from frontend
        score = data.get("score")
        total = data.get("total")
        deck_id = data.get("deck_id")

        # Retrieve associated deck
        deck = Deck.objects.get(id=deck_id)

        # Store quiz result in database
        Result.objects.create(
            user=request.user,
            deck=deck,
            score=score,
            total=total
        )
        # Return success response to frontend
        return JsonResponse({"status": "success"})

def submit_review(request, progress_id):
    progress = get_object_or_404(
        CardProgress,
        id=progress_id,
        user=request.user,
    )

    if request.method == "POST":
        rating = int(request.POST["rating"])
        review_card(progress, rating)

        messages.success(request, "Review saved")

    
    return redirect("study_deck", deck_id=progress.card.deck_id)

def overview(request):
    decks = Deck.objects.all()
    return render(request, 'overview.html', {'decks': decks})

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

def flashcards(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)
    cards = list(
    Card.objects.filter(deck=deck)
    .values("id", "question", "answer"))
    return render(request, 'Flashcards.html', {
        'deck': deck,
        'cards': cards
    })  

def manage_deck(request, deck_id):

    # Get selected deck
    deck = get_object_or_404(Deck, id=deck_id)

    # Get all cards in deck
    cards = Card.objects.filter(deck=deck)

    return render(request, 'manage_deck.html', {
        'deck': deck,
        'cards': cards
    })

@login_required
def create_deck(request):

    # If user submitted the form
    if request.method == "POST":
        form = DeckForm(request.POST)

        if form.is_valid():
            deck = form.save(commit=False)
            deck.owner = request.user
            deck.save()

            return redirect('decks', deck_id=deck.id)

    else:
        form = DeckForm()

    # If page is opened normally
    return render(request, 'create_deck.html', {"form": form})

@login_required
def study_deck(request, deck_id):

    # Allow users to access:
    # 1. Their own decks
    # 2. Default decks created by admin (owner is null)
    deck = get_object_or_404(
        Deck.objects.filter(
            Q(owner=request.user) |
            Q(is_default=True, owner__isnull=True)
        ),
        id=deck_id,
    )

    # Ensure All cards in the given deck have a progress row for this user
    # get_or_create prevents duplicate progress rows
    for card in deck.cards.all():
        CardProgress.objects.get_or_create(
            user=request.user,
            card=card
        )

    # Get due cards for this user and deck
    due_cards = get_due_cards(user=request.user, deck=deck)

    # Get next due card
    progress = due_cards.first()
    # Count remaining due cards for display
    remaining_count = due_cards.count()

    # Load study page with next due card and remaining count
    return render(request, "study_deck.html", {
        "deck":deck,
        "progress":progress,
        "remaining_count": remaining_count
    })

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

@login_required
def profile(request: HttpRequest) -> HttpResponse:
    """
    Loads the profile.html file and renders it with the Django template tags. 

    Args:
        request: Http Request Object

    Returns:
        HttpResponse Object with rendered HTML 
    """
    return render(request, 'account/profile.html', {})