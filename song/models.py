from django.db import models

from desert.storage import TencentStorage


class SongRecord(models.Model):
    id = models.BigAutoField(primary_key=True)
    song_id = models.IntegerField()
    user_id = models.IntegerField()
    score = models.IntegerField(default=0)
    best_score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class SongInfo(models.Model):
    song_id = models.BigAutoField(primary_key=True)
    song_name = models.CharField(max_length=100)
    song_author = models.CharField(max_length=100)
    score_author = models.CharField(max_length=100)
    difficulty = models.FloatField(max_length=20)
    level = models.CharField(max_length=20)
    song_file = models.FileField(storage=TencentStorage(), null=True)
