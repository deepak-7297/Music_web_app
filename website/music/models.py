from django.contrib.auth.models import User,Permission
from django.db import models
from django.urls import reverse

# Create your models here.
class Album(models.Model):
    artist=models.CharField(max_length=200)
    album_title=models.CharField(max_length=200)
    genre=models.CharField(max_length=200)
    album_logo=models.FileField()
    def get_absolute_url(self):
        return reverse('detail',kwargs={'pk':self.pk})

    def __str__(self):
        return self.album_title+'-' +self.artist

class Songs(models.Model):
    album=models.ForeignKey(Album ,on_delete=models.CASCADE)
    file_type=models.FileField()
    song_title=models.CharField(max_length=200)
    is_favourite=models.BooleanField(default=False)

    def __str__(self):
        return self.song_title
