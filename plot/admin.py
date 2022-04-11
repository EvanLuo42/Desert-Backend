from django.contrib import admin

from plot.models import Plot, PlotRead, Chapter, ChapterUnlock

admin.site.register(Plot)
admin.site.register(PlotRead)
admin.site.register(Chapter)
admin.site.register(ChapterUnlock)
