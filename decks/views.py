from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import  authentication, permissions
from rest_framework.permissions import IsAuthenticated

from rest_framework.authentication import TokenAuthentication

from .models import Deck, Value, Card
from .serializers import DeckSerializer, AddToDeckSerializer

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


@api_view(["POST"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def addToDeck(request):
    data = request.data.get('data')
    deck_slug = request.data.get("deck_slug")
    serializer = AddToDeckSerializer(data = data.get("values"), many=True)

    if (serializer.is_valid()):
        deck = get_object_or_404(Deck, slug = deck_slug)
        card = Card.objects.create(deck_id = deck.id)

        for value_field in serializer.validated_data:
            field_id = value_field["field_id"]
            value = value_field["value"]
            Value.objects.create(field_id=field_id, card_id=card.id, value=value)
    return Response()
