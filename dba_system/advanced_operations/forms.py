from django import forms

from advanced_operations.models import Tables


class TablesForm(forms.Form):
    tables = forms.MultipleChoiceField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tables = Tables.get_table_names()
        self.fields['tables'].choices = tuple((table_name['table_name'], table_name['table_name']) for table_name in tables)
