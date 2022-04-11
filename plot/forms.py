from django.forms import Form, fields
from django.utils.translation import gettext as _

from plot import models

Plot = models.Plot
Chapter = models.Chapter


class PlotForm(Form):
    plot_id = fields.IntegerField(
        required=True,
        error_messages={
            'required': _('Plot ID is required')
        }
    )

    def clean_plot_id(self):
        if Plot.objects.filter(plot_id=self.cleaned_data.get('plot_id')).exists():
            return self.cleaned_data.get('plot_id')
        else:
            raise ValueError(_('Plot does not exist'))


class ChapterForm(Form):
    chapter_id = fields.IntegerField(
        required=True,
        error_messages={
            'required': _('Chapter ID is required')
        }
    )

    def clean_chapter_id(self):
        if Chapter.objects.filter(chapter_id=self.cleaned_data.get('chapter_id')).exists():
            return self.cleaned_data.get('chapter_id')
        else:
            raise ValueError(_('Chapter does not exist'))
