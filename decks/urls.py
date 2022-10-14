from django.urls import path

from decks import views

urlpatterns = [
    path('get-my/', views.MyDecks.as_view()),
    path('get/<slug:deck_slug>/', views.DeckDetails.as_view()),
    path('add/', views.addToDeck),
]