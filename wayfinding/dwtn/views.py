from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import json
import sys

from .models import Category, Location

def index(request):
    category_list = Category.objects.all()
    context = {'category_list':category_list}
    return render(request, 'dwtn/index.html', context)
    
def detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    return render(request, 'dwtn/detail.html', {'category':category})
    
def location(request, location_name):
    location = get_object_or_404(Location, pk=location_id)
    return render(request, 'dwtn/location.html', {'location':location})

def make_json(request):
    
    if "runserver" not in sys.argv: # hackish way to test if we are on dev or production server
        cat_list = []
        loc_list = []
        root_dict = {}
        
        for category in Category.objects.all():
            cat_list.append({"id": category.pk, "name": category.category_name, "pin": category.pin, "color": category.color})
        for location in Location.objects.all():
            loc_list.append({"name": location.location_name, "lon": str(location.lon),
                             "lat": str(location.lat), "img": location.image, "details": location.details, "state": location.state, "catid": location.category_id})
        root_dict["categories"] = cat_list
        root_dict["locations"] = loc_list
        data = json.dumps(root_dict, indent=2)
        
        return HttpResponse(data, content_type='application/json')
    else: # if not on a production server, return static data for testing
        return render(request, 'dwtn/static_dump.json', content_type='application/json')
