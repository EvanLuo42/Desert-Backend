from django.forms import Form, fields
from django.utils.translation import gettext as _

from plot import models

Plot = models.Plot
Chapter = models.Chapter
Item = models.Item


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
            raise fields.ValidationError(_('Plot does not exist'))


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
            raise fields.ValidationError(_('Chapter does not exist'))


class ItemForm(Form):
    item_id = fields.UUIDField(
        required=True,
        error_messages={
            'required': _('Item ID is required')
        }
    )

    def clean_item_id(self):
        if Item.objects.filter(item_id=self.cleaned_data.get('item_id')).exists():
            return self.cleaned_data.get('item_id')
        else:
            raise fields.ValidationError(_('Item does not exist'))
