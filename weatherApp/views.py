from django.shortcuts import render
import urllib.request
import json
from urllib.error import URLError

def index(request):
    if request.method == 'POST':
        try:
            city = request.POST['city']
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=82e1d97441d016c4b6a72cda969b1900'
            source = urllib.request.urlopen(url).read()
            list_of_data = json.loads(source)
            
            if list_of_data.get('cod') == 200:  # Check if response code indicates success
                weather_data = {
                    "country_code" : str(list_of_data['sys']['country']),
                    "coordinate" :  str(list_of_data['coord']['lon'])+', '+str(list_of_data['coord']['lat']),
                    "temp" :        str(list_of_data['main']['temp'])+', '+'°C',
                    "pressure":     str(list_of_data['main']['pressure']),
                    "humidity" :    str(list_of_data['main']['humidity']),
                    "main" :        str(list_of_data['weather'][0]['main']),
                    "description" : str(list_of_data['weather'][0]['description']),
                    "icon" :        str(list_of_data['weather'][0]['icon']),
                }
                weather_data_list = [weather_data]
                print(weather_data_list)
            else:
                raise ValueError('City not found')

        except (URLError, ValueError, KeyError) as e:
            error_message = str(e)
            return render(request, "main/index.html", {'error_message': error_message})
            
    else:
        weather_data_list = []
    return render(request,"main/index.html",{'weather_data_list': weather_data_list})
