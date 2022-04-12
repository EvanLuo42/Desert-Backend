from django.contrib import admin

from plot.models import Plot, PlotRead, Chapter, ChapterUnlock, Item, CharacterUnlock, Character

admin.site.register(Plot)
admin.site.register(PlotRead)
admin.site.register(Chapter)
admin.site.register(ChapterUnlock)
admin.site.register(Item)
admin.site.register(CharacterUnlock)
admin.site.register(Character)
