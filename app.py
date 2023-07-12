##############################################################################
###   IMPORT LIBRARIES   #####################################################
import json
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template


##############################################################################
###   FETCH SECRETS   ########################################################
def GetValueFromJson(json_file, key):
   try:
       with open(json_file) as f:
           data = json.load(f)
           return data[key]
   except Exception as e:
       print("Error: ", e)


##############################################################################
###   FETCH DATA   ###########################################################
def FetchData(url_name):
    sitename = GetValueFromJson("secrets.json", "SITENAME")
    user_agent = {'User-agent': sitename} # Generate user-agent object (which is required by the api service)
    
    page = requests.get(url_name, headers = user_agent)

    if page.status_code != 200:
        print("Could not download url " + str(page.status_code))
    else: pass

    result = BeautifulSoup(page.text, "html.parser")

    return json.loads(result.text)

def GetWeatherDataFromSource():
    url_base = "https://api.met.no"
    url_parameters = "/weatherapi/locationforecast/2.0/compact?"
    url_lat = "lat=57"
    url_lon = "lon=12"

    weather_url = url_base + url_parameters + url_lat + "&" + url_lon

    return FetchData(weather_url)['properties']['timeseries']
# TODO: Write test to verify result is the dictionary expected, and that there are no missing values

def GetWeatherSymbolsFromSource():
    weather_symbol_url = 'https://api.met.no/weatherapi/weathericon/2.0/legends'

    return FetchData(weather_symbol_url)
# TODO: Write test to verify result is the dictionary expected

##############################################################################
###   CLEAN DATA  ############################################################
# TODO: Improve this code
def GetWeatherNextHour(dictionary):
    now = datetime.now()
    next_hour = (now + timedelta(hours=1)).strftime("%Y-%m-%dT%H")
    
    WeatherNextHour = []
    
    for row in dictionary[:]:
        date_time = str(row['time'][:13])
        if date_time == str(next_hour):
            WeatherNextHour.append(row)
        else: 
            pass
        
    return WeatherNextHour
            
def CreateApiWeatherNextHour(list):
    dict = {'date' : str(list[0]['time'][:10]),
            'time' : str(list[0]['time'][11:13]),
            'air_temperature' : float(list[0]['data']['instant']['details']['air_temperature']),
            'symbol_code' : str(list[0]['data']['next_1_hours']['summary']['symbol_code']),
            'precipitation_amount' : float(list[0]['data']['next_1_hours']['details']['precipitation_amount']),
            'wind_speed' : str(list[0]['data']['instant']['details']['wind_speed'])}
    
    return dict
    
#TODO: Convert string of date variable to time variable in order to change it into format eg. 1 march 2023. 

##############################################################################
###   CREATE FUNCTIONS FOR CLOTHES  ##########################################

def ClothesSuggestionByTemperaturePrecipitation(air_temperature, precipitation_amount):
    if -20 <= air_temperature < -10:
        return 'winter overall, wool or fleece layer, warm hat och warm gloves'
    elif -10 <= air_temperature < -5:
        return 'winter overall, warm hat and warm gloves'
    elif -5 <= air_temperature < 0:
        return 'fleece-lined rain gear, hat and gloves'
    elif 0 <= air_temperature < 5 and precipitation_amount == 0:
        return 'shell clothes + fleece clothes'
    elif 0 <= air_temperature < 5 and precipitation_amount > 0:
        return 'rain clothes + fleece clothes'
    elif 5 <= air_temperature < 10 and precipitation_amount == 0:
        return 'shell clothes'
    elif 5 <= air_temperature < 10 and precipitation_amount > 0:
        return 'rain clothes'
    elif 10 <= air_temperature < 20 and precipitation_amount == 0:
        return 'shell jacket'
    elif 10 <= air_temperature < 20 and precipitation_amount > 0:
        return 'rain clothes'
    elif 20 <= air_temperature < 30 and precipitation_amount == 0:
        return 'Whooop it´s summer'
    else:
        raise ValueError('something went wrong')

# TODO: Implement test



##############################################################################
###   CREATE APP  ############################################################

app = Flask(__name__)

@app.route('/nexthour')
def main():
    weather_dict_data = GetWeatherDataFromSource()
    weather_symbol_dict = GetWeatherSymbolsFromSource()
    WeatherNextHour = GetWeatherNextHour(weather_dict_data)
    ApiWeatherNextHour = CreateApiWeatherNextHour(WeatherNextHour)

    ApiWeatherNextHour['clothes'] = ClothesSuggestionByTemperaturePrecipitation(ApiWeatherNextHour['air_temperature'], ApiWeatherNextHour['precipitation_amount'])
    for key, value in weather_symbol_dict.items():
        if key == ApiWeatherNextHour['symbol_code'].split('_')[0]:
            ApiWeatherNextHour['symbol_text'] = value['desc_en'].lower()
        else:
            pass

    
    return render_template('index.html', 
                           date = ApiWeatherNextHour['date'],
                           time = ApiWeatherNextHour['time'],
                           air_temperature = ApiWeatherNextHour['air_temperature'],
                           symbol_text = ApiWeatherNextHour['symbol_text'],
                           precipitation_amount = ApiWeatherNextHour['precipitation_amount'],
                           wind_speed = ApiWeatherNextHour['wind_speed'],
                           clothes = ApiWeatherNextHour['clothes'])

if __name__ == '__main__':
    app.run()









