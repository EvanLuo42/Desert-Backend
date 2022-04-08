# -*- coding: utf-8 -*-
import math

from django.forms import Form, fields
from django.utils.translation import gettext as _

from song import models
from desert.utils import SHA256

SongInfo = models.SongInfo


class UploadScoreForm(Form):
    song_id = fields.IntegerField(
        required=True,
        error_messages={
            'required': _('Song ID can not be null.')
        }
    )

    score = fields.IntegerField(
        required=True,
        error_messages={
            'required': _('Score can not be null.')
        }
    )

    rank_point = fields.IntegerField(
        required=True,
        error_messages={
            'required': _('Rank point can not be null.')
        }
    )

    salt = fields.CharField(
        required=True,
        error_messages={
            'required': _('Salt can not be null.')
        }
    )

    magic = fields.CharField(
        required=True,
        error_messages={
            'required': _('Magic can not be null.')
        }
    )

    def clean_magic(self):
        sha256 = SHA256()
        magic = self.cleaned_data.get('magic')
        rank_point = self.data.get('rank_point')
        salt = self.data.get('salt')
        score = self.data.get('score')
        song_id = self.cleaned_data.get('song_id')

        if sha256.hash(str(rank_point + score + song_id) + salt) == magic:
            return magic
        else:
            raise fields.ValidationError(_('Magic is not correct.'))

    def clean_song_id(self):
        if SongInfo.objects.filter(song_id=self.cleaned_data.get('song_id')).exists():
            return self.cleaned_data.get('song_id')
        else:
            raise fields.ValidationError(_('Song ID is not exist.'))


class GetSongInfoForm(Form):
    song_id = fields.IntegerField(
        required=True,
        error_messages={
            'required': _('Song ID can not be null.')
        }
    )

    def clean_song_id(self):
        if SongInfo.objects.filter(song_id=self.cleaned_data.get('song_id')).exists():
            return self.cleaned_data.get('song_id')
        else:
            raise fields.ValidationError(_('Song ID is not exist.'))
