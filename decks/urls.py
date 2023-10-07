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
    path('copy-deck-structure/<str:deck_slug>/<str:new_deck_name>', views.copyDeckStructure),
    path('create-exam/<str:deck_slug>/', views.createExam),
    path('create-test/<str:deck_slug>/<int:cards_number>', views.createTest),
    path('create-quest/<str:deck_slug>/<int:cards_number>/<int:questions_limit>', views.createQuest),
]