import uuid

from django.db import models


class Chapter(models.Model):
    chapter_id = models.BigAutoField(primary_key=True)
    chapter_name = models.CharField(max_length=255)
    plot_id = models.IntegerField()


class Plot(models.Model):
    plot_id = models.BigAutoField(primary_key=True)
    plot_content = models.TextField()
    plot_title = models.CharField(max_length=255)


class ChapterUnlock(models.Model):
    id = models.BigAutoField(primary_key=True)
    chapter_id = models.IntegerField(null=True)
    user_id = models.IntegerField(null=True)


class PlotRead(models.Model):
    id = models.BigAutoField(primary_key=True)
    plot_id = models.IntegerField(null=True)
    user_id = models.IntegerField(null=True)


class Character(models.Model):
    character_id = models.BigAutoField(primary_key=True)
    character_name = models.CharField(max_length=255)


class CharacterUnlock(models.Model):
    id = models.BigAutoField(primary_key=True)
    character_id = models.IntegerField(null=True)
    user_id = models.IntegerField(null=True)


class Item(models.Model):
    item_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    item_name = models.CharField(max_length=255)

