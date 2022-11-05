from rest_framework import serializers

from .models import Deck, Field, Card, Value

class FieldSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Field
        fields = (
            "id",
            "name",
            "side",
            "position",
            "type",
            "fontSize"
        )


class ValueSerializer(serializers.ModelSerializer):
    field = FieldSerializer()
    id = serializers.IntegerField()
    class Meta:
        model = Value
        fields = (
            "id",
            "field",
            "value",
        )


class CardSerializer(serializers.ModelSerializer):
    values = ValueSerializer(many = True)
    class Meta:
        model = Card
        fields = (
            "id",
            "values",
        )


        
class DeckSerializer(serializers.ModelSerializer):
    fields = FieldSerializer(many = True)
    cards = CardSerializer(many = True)
   
    class Meta:
        model = Deck
        fields = (
            "id",
            "name",
            "user",
            "slug",
            "fields",
            "cards",
            "cards_number",
        )


class AddToDeckSerializer(serializers.Serializer):
    field_id = serializers.IntegerField()
    value = serializers.CharField()
    






class TestingSerializer(serializers.Serializer):
    card = CardSerializer()
    correct_answer = serializers.CharField()
    side = serializers.CharField(max_length = 5)
    answers = serializers.ListField(child = serializers.CharField(max_length = 255))
    
