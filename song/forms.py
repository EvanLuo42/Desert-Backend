from django.forms import Form, fields

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

    def clean_song_id(self):
        if SongInfo.objects.filter(song_id=self.cleaned_data.get('song_id')).exists():
            return self.cleaned_data.get('song_id')
        else:
            fields.ValidationError('Song ID is not exist.')


class GetSongInfoForm(Form):
    song_id = fields.IntegerField(
        required=True
    )

    def clean_song_id(self):
        if SongInfo.objects.filter(song_id=self.cleaned_data.get('song_id')).exists():
            return self.cleaned_data.get('song_id')
        else:
            fields.ValidationError('Song ID is not exist.')
