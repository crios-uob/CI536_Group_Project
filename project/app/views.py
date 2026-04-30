from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.

def test(request: HttpRequest) -> HttpResponse:
    """
    Loads an html file and renders it with the Django template tags. 

    Args:
        request: Http Request Object

    Returns:
        HttpResponse Object with rendered HTML 
    """
    return render(request, 'test.html', {'name': 'Jason'})


