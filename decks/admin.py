from django.contrib import admin

from .models import Deck, Field, Card, Value

admin.site.register(Deck)
admin.site.register(Field)
admin.site.register(Card)
admin.site.register(Value)
