from django.urls import path

from decks import views

urlpatterns = [
    path('get-my/', views.MyDecks.as_view()),
    path('get/<slug:deck_slug>/', views.DeckDetails.as_view()),
    path('add/', views.addToDeck),
    path('update/<slug:deck_slug>/<str:deck_name>/', views.updateDeckName),
    path('update/values/', views.updateDeckValues),
    path('update/fields/', views.updateDeckFields),
    path('update/remove-cards/', views.removeDeckCards)
]