from django.contrib.auth.models import AbstractUser
from django.db import models

import uuid

# Create your models here.


class User(AbstractUser):
    pass


class Artist(models.Model):
    name = models.CharField(max_length=64)
    


class Album(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=64)
    image_url = models.URLField(blank=True)


class Song(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=64)
    duration = models.DurationField()

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="songs")
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="songs")

    GENRE_CHOICES = [
        ('PO', 'Pop'),
        ('AL', 'Alternative'),
        ('RA', 'Rap'),
        ('DA', 'Dance'),
        ('EL', 'Electronic'),
        ('LA', 'Latin'),
        ('RB', 'R&B/Soul'),
        ('RO', 'Rock'),
        ('JA', 'Jazz'),
        ('ME', 'Metal'),
        ('CL', 'Classical'),
        ('RE', 'Reggae'),
        ('BL', 'Blues'),
    ]

    genre = models.CharField(max_length=2, blank=True, choices=GENRE_CHOICES)


class Playlist(models.Model):
    
    title = models.CharField(max_length=64)
    description = models.TextField()

    songs = models.ManyToManyField(Song, blank=True, related_name="in_playlists")