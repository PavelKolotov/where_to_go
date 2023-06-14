import json
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404
from places.models import Place, Image


# def show_start_page(request):
#     template = loader.get_template('index.html')
#     context = {}
#     rendered_page = template.render(context, request)
#     return HttpResponse(rendered_page)


def get_geo_json(request):
    places = Place.objects.all()
    geo_json = {
        "type": "FeatureCollection",
        "features": []
    }
    for place in places:
        imgs = []
        for image in place.images.all():
            imgs.append(str(image.image))
        features = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [place.coordinate_lng, place.coordinate_lat]
            },
            "properties": {
                "title": place.title,
                "placeId": place.id,
                "detailsUrl": 'static/places/moscow_legends.json',
                # "detailsUrl": {
                #     "title": place.title,
                #     "imgs": imgs,
                #     "description_short": place.description_short,
                #     "description_long": place.description_long,
                #         "coordinates": {
                #         "lng": place.coordinate_lng,
                #         "lat": place.coordinate_lat
                #     }
                # }
            }
        }
        geo_json['features'].append(features)
    places_geo_json = {
        'places': geo_json
    }
    return render(request, "index.html", context=places_geo_json)


def get_place(request, place_id):
    imgs = []
    place = get_object_or_404(Place, pk=place_id)
    for image in place.images.all():
        imgs.append(str(image.image))
    place_context = {
        "title": place.title,
        "imgs": imgs,
        "description_short": place.description_short,
        "description_long": place.description_long,
        "coordinates": {
            "lng": place.coordinate_lng,
            "lat": place.coordinate_lat
        }
    }

    return HttpResponse(place_context["title"])