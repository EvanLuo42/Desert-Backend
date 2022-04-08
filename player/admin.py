# -*- coding: utf-8 -*-
from django.contrib import admin

from player.models import Player
from song.models import Announcement

admin.site.register(Player)
admin.site.register(Announcement)
