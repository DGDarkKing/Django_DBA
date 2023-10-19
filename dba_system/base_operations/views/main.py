from django.shortcuts import redirect
from django.views.decorators.http import require_GET

from base_operations.models import Columns


@require_GET
def get_details(request, table_name):
    return redirect('table_structure', table_name=table_name)





