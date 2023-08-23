from app import app
from flask import render_template
from app import get_data
from app import suggest_clothes

@app.route('/nexthour')
def main():
#TODO: Implement exception messages for status != 200 here
#    try:
    weather_dict_data = get_data.GetWeatherDataFromSource()
#    except APIException as e:
#        return render_template('error.html', reason = str(e);         
    weather_symbol_dict = get_data.GetWeatherSymbolsFromSource()
    WeatherNextHour = get_data.GetWeatherNextHour(weather_dict_data)
    ApiWeatherNextHour = get_data.CreateApiWeatherNextHour(WeatherNextHour)

    ApiWeatherNextHour['clothes'] = suggest_clothes.ClothesSuggestionByTemperaturePrecipitation(ApiWeatherNextHour['air_temperature'], ApiWeatherNextHour['precipitation_amount'])
#TODO: Look up map function 
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