"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app import views

urlpatterns = [
    path('', views.dashboard,  name='dashboard'),
    path('admin/', admin.site.urls),

    path('accounts/', include('allauth.urls')),

    path("profile/", views.profile, name="profile"),
    path('overview/', views.overview,  name='overview'),
    path('analytics/', views.analytics, name='analytics'),
    path('decks/', views.decks,  name='decks'),
    path('deck/<int:deck_id>/manage/',views.manage_deck, name='manage_deck'),
    path('create-deck/', views.create_deck, name='create_deck'),
    path('deck/<int:deck_id>/add-card/', views.add_card, name='add_card'),
    path('card/<int:card_id>/edit/', views.edit_card, name='edit_card'),
    path('card/<int:card_id>/delete/', views.delete_card, name='delete_card'),
    path('settings/', views.user_settings,  name='settings'),

    path('flashcards/<int:deck_id>/', views.flashcards,  name='flashcards'),
    path("<int:deck_id>/study/", views.study_deck, name="study_deck"),
    path("review/<int:progress_id>/", views.submit_review, name="submit_review"),
    path('quiz/<int:deck_id>/', views.quiz, name='quiz'),
    path('quiz-mc/<int:deck_id>/', views.quiz_mc, name='quiz_mc'),
    path('save-result/', views.save_result, name='save_result'),

    path('test/', views.test,  name='test'),
]
