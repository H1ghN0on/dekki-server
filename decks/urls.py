# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import path

from decks import views

urlpatterns = [
    path('get-my/', views.MyDecks.as_view()),
    path('get/<str:deck_slug>/', views.DeckDetails.as_view()),
    path('add/', views.addToDeck),
    path('add-new/<str:deck_name>/', views.createDeck),
    path('update/<str:deck_slug>/<str:deck_name>/', views.updateDeckName),
    path('update/values/', views.updateDeckValues),
    path('update/fields/', views.updateDeckFields),
    path('update/remove-cards/', views.removeDeckCards),
    path('remove/<str:deck_slug>/', views.removeDeck),
    path('create-test/<str:deck_slug>/<int:cards_number>', views.createTest),
]