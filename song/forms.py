import math

from django.forms import Form, fields
from werkzeug.security import generate_password_hash, check_password_hash

from song import models

SongInfo = models.SongInfo


class UploadScoreForm(Form):
    song_id = fields.IntegerField(
        required=True,
        error_messages={
            'required': 'Song ID can not be null.'
        }
    )

    score = fields.IntegerField(
        required=True,
        error_messages={
            'required': 'Song ID can not be null.'
        }
    )

    rank_point = fields.IntegerField(
        required=True,
        error_messages={
            'required': 'Rank point can not be null.'
        }
    )

    magic = fields.IntegerField(
        required=False, # True
        error_messages={
            'required': 'Magic can not be null.'
        }
    )

    def clean_magic(self):
        magic = self.cleaned_data.get('magic')
        rank_point = self.changed_data.get('rank_point')
        score = self.cleaned_data.get('score')
        song_id = self.cleaned_data.get('song_id')

        if check_password_hash(magic, rank_point + score + song_id):
            return magic
        else:
            raise fields.ValidationError('Magic is not correct.')

    def clean_song_id(self):
        if SongInfo.objects.filter(song_id=self.cleaned_data.get('song_id')).exists():
            return self.cleaned_data.get('song_id')
        else:
            raise fields.ValidationError('Song ID is not exist.')


class GetSongInfoForm(Form):
    song_id = fields.IntegerField(
        required=True,
        error_messages={
            'required': 'Song ID can not be null.'
        }
    )

    def clean_song_id(self):
        if SongInfo.objects.filter(song_id=self.cleaned_data.get('song_id')).exists():
            return self.cleaned_data.get('song_id')
        else:
            raise fields.ValidationError('Song ID is not exist.')
