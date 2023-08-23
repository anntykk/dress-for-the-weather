##############################################################################
###   CREATE FUNCTIONS FOR CLOTHES  ##########################################

#TODO: Put this in to a table structure instead
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