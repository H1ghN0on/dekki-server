# Generated by Django 4.1.2 on 2022-10-25 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('decks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='field',
            name='name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='value',
            name='value',
            field=models.TextField(blank=True),
        ),
    ]