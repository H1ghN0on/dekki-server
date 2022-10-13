from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response


from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .models import Deck
from .serializers import DeckSerializer

class MyDecks(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        decks = Deck.objects.filter(user=request.user)
        serializer = DeckSerializer(decks, many = True)
        return Response(serializer.data)
    

class DeckDetails(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    def get_object(self, deck_slug):    
        try:
            return Deck.objects.get(slug=deck_slug)
        except Deck.DoesNotExist:
            raise Http404

    def get(self, request, deck_slug):
        deck = self.get_object(deck_slug)
        serializer = DeckSerializer(deck)
        return Response(serializer.data)