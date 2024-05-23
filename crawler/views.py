from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError
from datetime import datetime
from .crawler import crawl_page
from .models import WebResources
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

def health_check(request):
    # Check database connection
    db_conn = connections['default']
    try:
        db_conn.cursor()
    except OperationalError:
        return JsonResponse({'status': 'fail', 'database': 'unreachable'}, status=500)

    # You can add more checks here (e.g., external services, cache)
    
    return JsonResponse({'status': 'ok', 'time': datetime.now().isoformat()})

@csrf_exempt
def screenshots(request):
    if request.method == 'POST':
        url = request.POST.get('start_url')
        # print(request.body)
        if not url:
            return JsonResponse({'status': 'fail', 'message': 'start_url is required'}, status=400)
        depth = request.POST.get('number_of_links_to_follow', 1)
        return start_crawler(url, depth)
    if request.method == 'GET':
        id = request.GET.get('id')
        return get_resources(id)


def start_crawler(url, depth):
    id, crawled_data = crawl_page(url, depth)
    for url, pic in crawled_data:
        WebResources.objects.create(link=url, image_reference=pic)
    return JsonResponse({'status': 'ok', 'message': f'Crawler started for {url} with id {id}'})


def get_resources(id):
    resources = WebResources.objects.get(image_reference=f'{id}/{id}.png')
    return JsonResponse({'status': 'ok', 'message': 'Resources returned', 'resource': serializers.serialize('json', [resources])})
