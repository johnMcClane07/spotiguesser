from django.db import models

class QuizResult(models.Model):
    user = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    artist_name= models.CharField(max_length=255, null=True)
    score = models.IntegerField()
    elapsed_time = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)