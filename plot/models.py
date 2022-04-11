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
    chapter_id = models.IntegerField()
    user_id = models.IntegerField()


class PlotRead(models.Model):
    id = models.BigAutoField(primary_key=True)
    plot_id = models.IntegerField()
    user_id = models.IntegerField()
