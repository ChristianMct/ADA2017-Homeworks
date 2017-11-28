import re

LATITUDE = "latitude"
LONGITUDE = "longitude"

def hms2degrees(coord,beginning,ending,lat):
    if re.search(beginning+'(.*?)\|(.*)'+ending,coord):
        if re.search(beginning+'(.*?)\|(.*)'+ending,coord).group(3) != '':
            if re.search(beginning+'(.*?)\|(.*?)\|(.*)'+ending,coord).group(4) != '':
                Sec=float(re.search(beginning+'(.*?)\|(.*?)\|(.*)\|'+ending,coord).group(4))
                M = float(re.search(beginning+'(.*?)\|(.*?)\|(.*)\|'+ending,coord).group(3))
                H = float(re.search(beginning+'(.*?)\|(.*?)\|(.*)\|'+ending,coord).group(2))
            else:
                Sec=0
                M = float(re.search(beginning+'(.*?)\|(.*)\|'+ending,coord).group(3))
                H = float(re.search(beginning+'(.*?)\|(.*)\|'+ending,coord).group(2))
        else:
            M=0
            Sec=0
            H = float(re.search(beginning+'(.*?)\|(.*)'+ending,coord).group(2))
        d=(Sec/60+M)/60+H
        if ending in ['S','W']:
            d=-d
        return d
    elif re.search('(N|S)\s(.*)°(.*)\′(.*)\″\s(E|W)\s(.*)°(.*)\′(.*)\″',coord):
        if lat=='lat':
            Hlat = float(re.search('(N|S)\s(.*)°(.*)\′(.*)\″\s(E|W)\s(.*)°(.*)\′(.*)\″',coord).group(2))
            Mlat = float(re.search('(N|S)\s(.*)°(.*)\′(.*)\″\s(E|W)\s(.*)°(.*)\′(.*)\″',coord).group(3))
            Slat = float(re.search('(N|S)\s(.*)°(.*)\′(.*)\″\s(E|W)\s(.*)°(.*)\′(.*)\″',coord).group(4))
            lat = (Slat/60+Mlat)/60+Hlat
            if re.search('(N|S)\s(.*)°(.*)\′(.*)\″\s(E|W)\s(.*)°(.*)\′(.*)\″',coord).group(1)=='S':
                lat = -lat
            return lat
        if lat=='long':
            Hlat = float(re.search('(N|S)\s(.*)°(.*)\′(.*)\″\s(E|W)\s(.*)°(.*)\′(.*)\″',coord).group(6))
            Mlat = float(re.search('(N|S)\s(.*)°(.*)\′(.*)\″\s(E|W)\s(.*)°(.*)\′(.*)\″',coord).group(7))
            Slat = float(re.search('(N|S)\s(.*)°(.*)\′(.*)\″\s(E|W)\s(.*)°(.*)\′(.*)\″',coord).group(8))
            lat = (Slat/60+Mlat)/60+Hlat
            if re.search('(N|S)\s(.*)°(.*)\′(.*)\″\s(E|W)\s(.*)°(.*)\′(.*)\″',coord).group(5)=='W':
                lat = -lat
            return lat
    return 0


def get_coordinates(coord_string):
    if not coord_string:
        return {}

    coord_string=coord_string.strip()
    try:
        latitude = hms2degrees(coord_string, '(Coord|coord)\|','(N|S)','lat')
        longitude = hms2degrees(coord_string, '(N|S)\|','(E|W)\|','long')
        if latitude == 0:
            if longitude == 0:
                if re.search('(Coord|coord)\|(.*)\|(N|S)\|(.*)\|(E|W)\|',coord_string):
                    latitude = float(re.search('(Coord|coord)\|(.*)\|(N|S)\|(.*)\|(E|W)\|',coord_string).group(2))
                    longitude = float(re.search('(Coord|coord)\|(.*)\|(N|S)\|(.*)\|(E|W)\|',coord_string).group(4))
                    if re.search('(Coord|coord)\|(.*)\|(N|S)\|(.*)\|(E|W)\|',coord_string).group(3) == 'S':
                        latitude=-latitude
                    if re.search('(Coord|coord)\|(.*)\|(N|S)\|(.*)\|(E|W)\|',coord_string).group(5) == 'W':
                        longitude=-longitude
                elif re.search('(Coord|coord)\|(.*)?\|',coord_string):
                    latitude = float(re.search('(.*)\|(.*)',re.search('(Coord|coord)\|(.*)?\|(.*)?\|',coord_string).group(2)).group(1))
                    longitude = float(re.search('(.*)\|(.*)',re.search('(Coord|coord)\|(.*)?\|(.*)?\|',coord_string).group(2)).group(2))
        return {'latitude': (latitude), 'longitude': (longitude), 'source': coord_string}
    except:
        try:
            if re.search('(Coord|coord)\|(.*)\|(N|S)\|(.*)\|(E|W)\|',coord_string):
                latitude = float(re.search('(Coord|coord)\|(.*)\|(N|S)\|(.*)\|(E|W)\|',coord_string).group(2))
                longitude = float(re.search('(Coord|coord)\|(.*)\|(N|S)\|(.*)\|(E|W)\|',coord_string).group(4))
                if re.search('(Coord|coord)\|(.*)\|(N|S)\|(.*)\|(E|W)\|',coord_string).group(3) == 'S':
                    latitude=-latitude
                if re.search('(Coord|coord)\|(.*)\|(N|S)\|(.*)\|(E|W)\|',coord_string).group(5) == 'W':
                    longitude=-longitude
                return {'latitude': (latitude), 'longitude': (longitude), 'source': coord_string}
            elif re.search('(Coord|coord)\|(.*)?\|',coord_string):
                latitude = float(re.search('(.*?)\|(.*?)\|',re.search('(Coord|coord)\|(.*)?\|(.*)',coord_string).group(2)).group(1))
                longitude = float(re.search('(.*?)\|(.*?)\|',re.search('(Coord|coord)\|(.*)?\|(.*)',coord_string).group(2)).group(2))
                return {'latitude': (latitude), 'longitude': (longitude), 'source': coord_string}
            return {'source':(coord_string)}
        except:
            return {'source':(coord_string)}
        

def get_features(battle_json):

    coord_str = battle_json["infobox"].get("coordinates", "").strip()
    src = "ib:"
    if not coord_str:
        coord_str = battle_json.get("coordinates", None)
        src = "ext:"

    coord_parsed = get_coordinates(coord_str)

    return {
        LATITUDE: coord_parsed.get("latitude"),
        LONGITUDE: coord_parsed.get("longitude"),
        "source": src+str(coord_str)
    }
