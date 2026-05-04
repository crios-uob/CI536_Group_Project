from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

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

def decks(request: HttpRequest) -> HttpResponse:
    """
    Loads the decks.html file and renders it with the Django template tags. 

    Args:
        request: Http Request Object

    Returns:
        HttpResponse Object with rendered HTML 
    """
    return render(request, 'decks.html', {})

def dashboard(request: HttpRequest) -> HttpResponse:
    """
    Loads the dashboard.html file and renders it with the Django template tags. 

    Args:
        request: Http Request Object

    Returns:
        HttpResponse Object with rendered HTML 
    """
    return render(request, 'dashboard.html', {})

def overview(request: HttpRequest) -> HttpResponse:
    """
    Loads the overview.html file and renders it with the Django template tags. 

    Args:
        request: Http Request Object

    Returns:
        HttpResponse Object with rendered HTML 
    """
    return render(request, 'overview.html', {})

def flashcards(request: HttpRequest) -> HttpResponse:
    """
    Loads the flashcards.html file and renders it with the Django template tags. 

    Args:
        request: Http Request Object

    Returns:
        HttpResponse Object with rendered HTML 
    """
    return render(request, 'Flashcards.html', {})

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