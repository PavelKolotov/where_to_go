from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from places.models import Place


def get_index_page(request):
    places = Place.objects.all()
    features = []
    for place in places:
        features.append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [place.coordinate_lng, place.coordinate_lat]
            },
            'properties': {
                'title': place.title,
                'placeId': place.id,
                'detailsUrl': reverse('place_name', args=(place.id, )),
            }
        })

    context = {
        'places': {
            'type': 'FeatureCollection',
            'features': features
        }
    }
    return render(request, 'index.html', context=context)


def get_place(request, place_id):
    imgs = []
    place = get_object_or_404(Place, pk=place_id)
    for image in place.images.all():
        imgs.append(image.image.url)
    place_context = {
        'title': place.title,
        'imgs': imgs,
        'description_short': place.description_short,
        'description_long': place.description_long,
        'coordinates': {
            'lng': place.coordinate_lng,
            'lat': place.coordinate_lat
        }
    }
    return JsonResponse(place_context, json_dumps_params={'ensure_ascii': False, 'indent': 4})
