from itertools import islice
import random


from sqlite3 import DataError, OperationalError
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import  authentication, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .models import Deck, Field, Value, Card
from .serializers import  CardSerializer, DeckSerializer, AddToDeckSerializer, \
    FieldSerializer, TestingSerializer, ValueSerializer, QuestSerializer, DeckInfoSerializer

class MyDecks(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        decks = Deck.objects.filter(user=request.user)
        serializer = DeckInfoSerializer(decks, many = True)
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

class DeckDetailsInfo(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    def get_object(self, deck_slug):    
        try:
            return Deck.objects.get(slug=deck_slug)
        except Deck.DoesNotExist:
            raise Http404

    def get(self, request, deck_slug):
        deck = self.get_object(deck_slug)
        serializer = DeckInfoSerializer(deck)
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


@api_view(["DELETE"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def removeDeck(request, deck_slug):
    Deck.objects.filter(slug=deck_slug).delete()
    return Response()

@api_view(["PUT"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def updateDeckName(request, deck_name, deck_slug):
    deck = Deck.objects.get(slug = deck_slug)
    deck.name = deck_name
    deck.save()
    return Response(deck.slug)

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


@api_view(["GET"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def copyDeckStructure(request, deck_slug, new_deck_name):
    deck = Deck.objects.get(slug = deck_slug)
    new_deck = Deck.objects.create(
        name = new_deck_name,
        user = request.user,
    )
    fields = Field.objects.filter(deck_id = deck.id)
    for field in fields:
        Field.objects.create(
            side = field.side,
            position =  field.position,
            name =  field.name,
            type = field.type,
            fontSize =  field.fontSize,
            deck_id = new_deck.id, 
        )
    serializer = DeckSerializer(new_deck)
    return Response(serializer.data)

def generateTest(deck, cards, card_indices):
    sides = ["front", "back"]
    test = list()
    for card_index in card_indices:

        random_side = random.choice(sides)
        known_side  = "back" if random_side == "front" else "front"

        known_card = cards[card_index]
        random_fields = Field.objects.filter(deck = deck, side = known_side)
        random_values = set()
   
        while len(random_values) != 3:
            random_card = random.choice(cards)
            if (random_card.id != known_card.id):
                random_value = Value.objects.filter(card = random_card, field = random.choice(random_fields))
                one_random_value = random.choice(random_value)

                if (one_random_value.value):
                    random_values.add(random.choice(random_value))
                
        correct_value = ""
        while not correct_value:
            correct_values = Value.objects.filter(card = known_card, field = random.choice(random_fields))
            one_random_value = random.choice(correct_values)
            if (one_random_value.value):
                correct_value = random.choice(correct_values)
        

        random_values.add(correct_value)
        random.shuffle(list(random_values))
       
        test.append(
            dict({
                "correct_answer": correct_value,
                "card": known_card,
                "side": random_side,
                "answers": random_values
            })
        ) 
    return test

def generateQuest(deck, cards, card_indices):
    sides = ["front", "back"]
    test = list()
    for card_index in card_indices:
        random_side = random.choice(sides)
        known_side  = "back" if random_side == "front" else "front"

        known_card = cards[card_index]
        random_fields = Field.objects.filter(deck = deck, side = known_side)
        correct_values = Value.objects.filter(card = known_card, field__in = random_fields)
        correct_values_arr = list()
        for value in correct_values:
            correct_values_arr.extend(value.value.split(", "))

        test.append(
            dict({
                "card": known_card,
                "side": random_side,
                "answers": correct_values_arr
            })
        )
    return test



@api_view(["GET"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def createExam(request, deck_slug):
    deck = Deck.objects.get(slug = deck_slug)
    cards  = Card.objects.filter(deck__slug = deck_slug)
    indices = list(range(cards.count()))
    random.shuffle(indices)
    test = generateTest(deck, cards, indices)
    serializer = TestingSerializer(test, many=True)
    return Response(serializer.data)
        


@api_view(["GET"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def createTest(request, deck_slug, cards_number):
    QUESTIONS_NUMBER = 100
    deck = Deck.objects.get(slug = deck_slug)
    cards  = Card.objects.filter(deck__slug = deck_slug).order_by("-id")[:cards_number][::-1]
    indices = list(range(cards_number))
    random.shuffle(indices)
    test = generateTest(deck, cards, indices[0:QUESTIONS_NUMBER])
    serializer = TestingSerializer(test, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def createQuest(request, deck_slug, cards_number, questions_limit):
    questions_number = questions_limit
    deck = Deck.objects.get(slug = deck_slug)

    if (questions_number == 0):
        questions_number = deck.cards_number()

    cards  = Card.objects.filter(deck__slug = deck_slug).order_by("-id")[:cards_number][::-1]
    indices = list(range(cards_number))
    random.shuffle(indices)
    test = generateQuest(deck, cards, indices[0:questions_number])
    serializer = QuestSerializer(test, many=True)
    return Response(serializer.data)