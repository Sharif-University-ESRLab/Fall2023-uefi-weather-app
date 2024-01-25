import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_401_UNAUTHORIZED
from rest_framework.views import APIView


def get_weather_to_status(weather_info):
    status = str(weather_info['weather'][0]['main']).lower()
    mist_list = ('mist', 'smoke', 'haze', 'dust', 'fog', 'sand', 'ash', 'squall', 'tornado')
    if status in mist_list:
        return 'mist'
    return status


def get_weather_by_geo_location(lat, lon):
    try:
        base_url = "https://api.openweathermap.org/data/2.5/onecall"
        params = {
            "lat": lat,
            "lon": lon,
            "exclude": "minutely,hourly",
            "units": "metric",
            "appid": settings.OPEN_WEATHER_MAP_API_TOKEN
        }

        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        weather = data['daily'][0]
        output = {
            "temp_day": str(weather['temp']['day']),
            "wind_speed": str(weather['wind_speed']),
            "humidity": str(weather['humidity']),
            "status": get_weather_to_status(weather),
            "description": str(weather['weather'][0]['description'])
        }
        return ','.join(list(output.values()))
    except Exception as e:
        print(e)
        return None


def get_geo_location(location_name):
    if not location_name:
        return None
    try:
        base_url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{location_name}.json"
        params = {
            "access_token": settings.MAP_BOX_API_TOKEN
        }
        response = requests.get(base_url, params=params)
        response.raise_for_status()

        data = response.json()
        geo_loc_arr = data['features'][0]['center']
        geo_loc = {
            "lat": str(geo_loc_arr[1]),
            "lon": str(geo_loc_arr[0]),
            "loc": data['features'][0]['text']
        }
        return geo_loc
    except Exception as e:
        print(e)
        return None


def get_weather_by_location_name(location_name):
    location = get_geo_location(location_name)

    if location:
        return get_weather_by_geo_location(location['lat'], location['lon'])
    else:
        return None


class DemoAPIView(APIView):

    def get(self, request):
        token = request.headers.get('Auth')
        if not (token and token == settings.USER_API_TOKEN):
            return Response(data='You are not allowed.', status=HTTP_401_UNAUTHORIZED)
        location = request.GET.get('location')
        weather_info = get_weather_by_location_name(location)
        if not weather_info:
            return Response(data='There was a problem', status=HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=weather_info, status=HTTP_200_OK)
