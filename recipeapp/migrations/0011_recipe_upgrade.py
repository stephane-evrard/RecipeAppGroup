# Generated by Django 3.2.8 on 2021-10-21 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipeapp', '0010_auto_20211021_0801'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='upgrade',
            field=models.BooleanField(default=False),
        ),
    ]
