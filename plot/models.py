import uuid

from django.db import models
from django.utils.translation import gettext as _

from desert.storage import ImageStorage


class Chapter(models.Model):
    chapter_id = models.BigAutoField(primary_key=True, verbose_name=_('Chapter ID'))
    chapter_name = models.CharField(max_length=255, verbose_name=_('Chapter name'))
    plot_id = models.IntegerField(verbose_name=_('Plot ID'))

    class Meta:
        verbose_name = _('Chapter')
        verbose_name_plural = verbose_name


class Plot(models.Model):
    plot_id = models.BigAutoField(primary_key=True, verbose_name=_('Plot ID'))
    plot_content = models.TextField(verbose_name=_('Plot content'))
    plot_title = models.CharField(max_length=255, verbose_name=_('Plot title'))

    class Meta:
        verbose_name = _('Plot')
        verbose_name_plural = verbose_name


class ChapterUnlock(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name=_('ID'))
    chapter_id = models.IntegerField(null=True, verbose_name=_('Chapter ID'))
    user_id = models.IntegerField(null=True, verbose_name=_('User ID'))

    class Meta:
        verbose_name = _('Chapter Unlock')
        verbose_name_plural = verbose_name


class PlotRead(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name=_('ID'))
    plot_id = models.IntegerField(verbose_name=_('Plot ID'))
    user_id = models.IntegerField(verbose_name=_('User ID'))

    class Meta:
        verbose_name = _('Plot Read')
        verbose_name_plural = verbose_name


class Character(models.Model):
    character_id = models.BigAutoField(primary_key=True, verbose_name=_('Character ID'))
    character_name = models.CharField(max_length=255, verbose_name=_('Character name'))
    character_image = models.FileField(storage=ImageStorage(), verbose_name=_('Character image'))

    class Meta:
        verbose_name = _('Character')
        verbose_name_plural = verbose_name


class CharacterUnlock(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name=_('ID'))
    character_id = models.IntegerField(null=True, verbose_name=_('Character ID'))
    user_id = models.IntegerField(null=True, verbose_name=_('User ID'))

    class Meta:
        verbose_name = _('Character Unlock')
        verbose_name_plural = verbose_name


class Item(models.Model):
    item_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, verbose_name=_('Item ID'))
    item_name = models.CharField(max_length=255, verbose_name=_('Item name (type + id)'))

    class Meta:
        verbose_name = _('Item')
        verbose_name_plural = verbose_name

