from django.contrib import admin

from song import models

admin.site.register(models.SongInfo)
admin.site.register(models.SongRecord)
admin.site.register(models.SongUnlock)
