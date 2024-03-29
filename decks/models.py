from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

from common.utils.unique_slugify import unique_slugify

class Deck(models.Model):
    user = models.ForeignKey(User, related_name="decks", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    def save(self, **kwargs):
        unique_slugify(self, self.name)
        super(Deck, self).save(**kwargs)


    def cards_number(self):
        cards_number = self.cards.count()
        return cards_number
        

    def __str__(self):
        return self.name


class Field(models.Model):

    class Meta:
        ordering = ["id"]

    class DeckSide(models.TextChoices):
        FACE = 'front', 'front'
        BACK = 'back', 'back'

    class FieldType(models.TextChoices):
        MAIN = 'main', 'main'
        SECONDARY = 'secondary', 'secondary'

    side = models.CharField(max_length = 5, choices = DeckSide.choices)
    position = models.PositiveSmallIntegerField()
    name = models.CharField(max_length = 255, blank = True)
    type = models.CharField(max_length = 9, choices = FieldType.choices)
    fontSize = models.PositiveSmallIntegerField()
    deck = models.ForeignKey(Deck, related_name="fields", on_delete=models.CASCADE)   

    def __str__(self):
        return self.name

class Card(models.Model):

    class Meta:
        ordering = ["id"]

    deck = models.ForeignKey(Deck, related_name="cards", on_delete=models.CASCADE)

    def __str__(self):
        return "Карта " + str(self.id)

class Value(models.Model):

    class Meta:
        ordering = ["id"]

    field = models.ForeignKey(Field, related_name="values", on_delete=models.CASCADE)
    card = models.ForeignKey(Card, related_name="values", on_delete=models.CASCADE)
    value = models.TextField(blank = True)

    def __str__(self):
        return self.value