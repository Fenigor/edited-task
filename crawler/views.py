from django.shortcuts import render

from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError
from datetime import datetime

def health_check(request):
    # Check database connection
    db_conn = connections['default']
    try:
        db_conn.cursor()
    except OperationalError:
        return JsonResponse({'status': 'fail', 'database': 'unreachable'}, status=500)

    # You can add more checks here (e.g., external services, cache)
    
    return JsonResponse({'status': 'ok', 'time': datetime.now().isoformat()})
