# Generated by Django 5.1.2 on 2024-11-20 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizresult',
            name='artist_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]