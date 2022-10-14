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
        )


class AddToDeckSerializer(serializers.Serializer):
    field_id = serializers.IntegerField()
    value = serializers.CharField()
    