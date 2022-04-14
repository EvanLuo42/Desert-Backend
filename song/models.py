from django.db import models

from desert.storage import SongStorage, ImageStorage
from django.utils.translation import gettext as _


class SongRecord(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name=_('ID'))
    song_id = models.IntegerField(verbose_name=_('Song ID'))
    user_id = models.IntegerField(verbose_name=_('User ID'))
    score = models.IntegerField(default=0, verbose_name=_('Score'))
    best_score = models.IntegerField(default=0, verbose_name=_('Best Score'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))

    class Meta:
        verbose_name = _('Song Record')
        verbose_name_plural = verbose_name


class SongInfo(models.Model):
    song_id = models.BigAutoField(primary_key=True, verbose_name=_('Song ID'))
    song_name = models.CharField(max_length=100, verbose_name=_('Song name'))
    song_author = models.CharField(max_length=100, verbose_name=_('Song author'))
    score_author = models.CharField(max_length=100, verbose_name=_('Score author'))
    background_image_author = models.CharField(max_length=100, verbose_name=_('Background image author'))
    difficulty = models.FloatField(max_length=20, verbose_name=_('Difficulty'))
    level = models.CharField(max_length=20, verbose_name=_('Level'))
    chapter_id = models.IntegerField(verbose_name=_('Chapter ID'))
    plot_id = models.IntegerField(verbose_name=_('Plot ID'))
    song_file = models.FileField(storage=SongStorage(), verbose_name=_('Song file'))
    image_file = models.FileField(storage=ImageStorage(), verbose_name=_('Image file'))
    file_md5 = models.CharField(max_length=128, verbose_name=_('File MD5'))

    class Meta:
        verbose_name = _('Song Info')
        verbose_name_plural = verbose_name


class SongUnlock(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name=_('ID'))
    song_id = models.IntegerField(verbose_name=_('Song ID'))
    user_id = models.IntegerField(verbose_name=_('User ID'))

    class Meta:
        verbose_name = _('Song Unlock')
        verbose_name_plural = verbose_name


class Announcement(models.Model):
    announcement_id = models.BigAutoField(primary_key=True, verbose_name=_('Announcement ID'))
    content = models.TextField(verbose_name=_('Content'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))

    class Meta:
        verbose_name = _('Announcement')
        verbose_name_plural = verbose_name
