import mwparserfromhell as mw
from .feature_utils import isfloat, get_templates

LATITUDE = "latitude"
LONGITUDE = "longitude"

CARDINALS = {"N", "S", "E", "W"}

# Deserialize coordinates
def split_coords(params):
    coords = list()
    acc = list()
    for p in params:
        if not p in CARDINALS:
            acc.append(p)
        else:
            coords.append(acc+[p])
            acc = list()
    return coords[0], coords[1]


# Converts from degree, minute second in any cardinal direction to degree N-E
def dms2dec(coord):
    dms = coord[:-1]
    sign = -1 if coord[-1] in {"S", "W"} else 1
    return sign*sum([float(a)*b for a, b in zip(dms, [1, 1/60, 1/3600])])


def get_coords_data(tpl):

    if not tpl:
        return None, None

    # gets rid of some useless params
    params = [str(param).strip() for param in tpl.params if isfloat(param) | (str(param).strip() in CARDINALS)]

    # coord implicitly in decimal, N-E format
    if not CARDINALS & set(params):
        return float(params[0]), float(params[1])

    # split serialized list
    lat, long = split_coords(params)

    # converts from dms to dec format
    return dms2dec(lat), dms2dec(long)


def get_features(battle_json):
    # Prioritize page level coords
    tpls = get_templates(mw.parse(battle_json.get("coordinates", battle_json["infobox"].get("coordinates"))), "coord")

    if tpls:
        latitude, longitude = get_coords_data(tpls[0])
    else:
        latitude, longitude = None, None

    return {
        LATITUDE: latitude,
        LONGITUDE: longitude,
    }
