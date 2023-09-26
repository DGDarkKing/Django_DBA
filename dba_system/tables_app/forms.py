from django import forms
from django.core import validators


class CreateTableForm(forms.Form):
    table_name = forms.CharField(
        min_length=1,
        max_length=63,
        validators=[
            validators.RegexValidator(
                '[^A-z_0-9]',
                inverse_match=True
            ),
        ]
    )
