from django.core.cache import cache
from django.forms import Form, fields
from django.utils.translation import gettext as _


class ValidTokenForm(Form):
    token = fields.CharField(
        required=True,
        error_messages={
            'required': _('Token is required.')
        }
    )

    uid = fields.IntegerField(
        required=True,
        error_messages={
            'required': _('User ID is required.')
        }
    )

    def clean_token(self):
        if cache.get(self.cleaned_data.get('uid')) is not None:
            if cache.get(self.cleaned_data.get('uid')) == self.cleaned_data.get('token'):
                return self.cleaned_data.get('token')
            else:
                raise fields.ValidationError(_('Token is invalid.'))
        else:
            raise fields.ValidationError(_('Token is invalid.'))
