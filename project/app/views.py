from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.

def load(request: HttpRequest, html_filename: str, tags: dict[str, str]) -> HttpResponse:
    """
    Loads an html file and renders it with the Django template tags. 

    Args:
        request: Http Request Objec
        html_filename: The filename of the html file to be loaded
        tags: A dict of tags to showing what each tag should be defined as 

    Returns:
        HttpResponse Object with rendered HTML 
    """
    return render(request, html_filename, tags)


