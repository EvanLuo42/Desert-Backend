from django.db import models

from desert.storage import SongStorage, ImageStorage


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
    chapter_id = models.IntegerField()
    plot_id = models.IntegerField()
    song_file = models.FileField(storage=SongStorage(), null=True)
    image_file = models.FileField(storage=ImageStorage(), null=True)
    file_md5 = models.CharField(max_length=128, null=True)


class SongUnlock(models.Model):
    id = models.BigAutoField(primary_key=True)
    song_id = models.IntegerField()
    user_id = models.IntegerField()


class Announcement(models.Model):
    announcement_id = models.BigAutoField(primary_key=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
