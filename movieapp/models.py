from django.db import models
import uuid

class Movie(models.Model):
    id = models.AutoField(primary_key=True, null=False, unique=True)
    name = models.CharField(max_length=100, unique=True, null=False)
    genre = models.CharField(default='horror', max_length=100)
    
    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Movie'


class User(models.Model):
    id = models.AutoField(primary_key=True, null=False, unique=True)
    username = models.CharField(max_length=100, unique=True, null=False)
    password = models.CharField(max_length=255, null=False)

    def __str__(self) -> str:
        return self.username

    class Meta:
        verbose_name = 'User'
        

class MovieCollection(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, null=False, unique=True)
    title = models.CharField(max_length=100, unique=True, null=False)
    movies = models.ManyToManyField(Movie, related_name='movies')
    description = models.TextField()
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='movie_collections')
    
    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Movie collection'


class RequestCount(models.Model):
    count = models.IntegerField(default=0)

