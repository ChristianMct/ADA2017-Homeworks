def get_country(place_string):
    try:
        return country
    except:
        return {'source':(place_string)}