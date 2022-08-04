from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Movies(models.Model):
    movie_name = models.CharField( max_length=512)
    genre = models.CharField(max_length=100)
    rating = models.FloatField()
    release_date = models.IntegerField(blank=True)

    
    def __str__(self) -> str:
        return self.movie_name


class Reviewes(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()


    def __str__(self) -> str:
        return self.content