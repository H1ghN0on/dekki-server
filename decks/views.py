from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import  authentication, permissions
from rest_framework.permissions import IsAuthenticated

from rest_framework.authentication import TokenAuthentication

from .models import Deck, Field, Value, Card
from .serializers import CardSerializer, DeckSerializer, AddToDeckSerializer, FieldSerializer, ValueSerializer

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


@api_view(["GET"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def createDeck(request, deck_name):
    deck = Deck.objects.create(
        name = deck_name,
        user = request.user,

    )
    return Response(deck.slug)

@api_view(["PUT"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def updateDeckName(request, deck_name, deck_slug):
    Deck.objects.filter(slug = deck_slug).update(name = deck_name)
    return Response()

@api_view(["POST"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def updateDeckValues(request):
    data = request.data.get('data')
    data_serializer = ValueSerializer(data = data, many = True)
    value = Value.objects.all()[0]

    if (data_serializer.is_valid()):
        for value in data_serializer.validated_data:
            new_value = value["value"]
            value_id = value["id"]
            Value.objects.filter(id = value_id).update(value = new_value)
    return Response()


@api_view(["POST"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def removeDeckCards(request):
    data = request.data.get('data')
    
    for id in data:
        card = Card.objects.get(id = id)
        card.delete()
   
    return Response()



@api_view(["POST"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def updateDeckFields(request):
    data = request.data.get('data')
    deck_slug = request.data.get("deck_slug")
    deck = Deck.objects.get(slug = deck_slug)
    data_serializer = FieldSerializer(data = data, many = True)
    cards = Card.objects.filter(deck = deck)
    fields = Field.objects.filter(deck = deck)
    updatedFields = []
   
    if (data_serializer.is_valid()):
        print(data_serializer.validated_data)
        for field in data_serializer.validated_data:
            if (field["id"] < 0):
                del field["id"]
                field["decks_field"] = deck.id
                field_db = Field.objects.create(
                    side = field["side"],
                    position =  field["position"],
                    name =  field["name"],
                    type = field["type"],
                    fontSize =  field["fontSize"],
                    deck_id = deck.id, 
                )
                updatedFields.append(field_db.id)
                for card in cards:
                    Value.objects.create(
                        value = "",
                        card = card,
                        field = field_db
                    )
            else:
                Field.objects.filter(id = field["id"]).update(
                    side = field["side"],
                    position =  field["position"],
                    name =  field["name"],
                    type = field["type"],
                    fontSize =  field["fontSize"],
                )
                updatedFields.append(field["id"])
 
        for field in fields:
            if (field.id not in updatedFields):
                field.delete()

    return Response()


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
