from django import forms

from base_operations.models import Columns


class ColumnDataForm(forms.Form):
    name = forms.CharField(max_length=63)
    type = forms.ChoiceField(
        choices=tuple((type[0], type[0]) for type in Columns.get_column_types())
    )
    limit = forms.IntegerField(
        label='Precision limit',
        required=False,
    )
    num_scale = forms.IntegerField(
        label='Numeric scale',
        required=False,
    )
    not_null = forms.BooleanField(required=False)
    default_value = forms.CharField(required=False)


class PrimaryKeyDataForm(forms.Form):
    name = forms.CharField(max_length=63)
    columns = forms.MultipleChoiceField(
        choices=('', '')
    )

    def __init__(self, *args, table_name, **kwargs):
        super().__init__(*args, **kwargs)
        columns = tuple((column['column_name'], column['column_name']) for column in Columns.get_columns(table_name))
        self.fields['columns'].choices = columns

class IndexDataForm(forms.Form):
    name = forms.CharField(max_length=63)
    is_unique = forms.BooleanField(required=False)
    columns = forms.MultipleChoiceField(
    )

    def __init__(self, *args, table_name, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['columns'].choices = tuple((type['column_name'], type['column_name']) for type in Columns.get_columns(table_name))
