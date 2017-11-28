import mwparserfromhell as mw
import re
from .feature_utils import get_templates
from collections import OrderedDict

COMBATANT_FIRST = ["combatant_first_1", "combatant_first_2", "combatant_first_3"]
COMBATANT_LISTS = ["combatant_list_1", "combatant_list_2", "combatant_list_3"]

ACRONYMS_PAT = re.compile("\b(?:[A-Z]\.?){2,}")


def get_combatants(battle_infobox_json):
    return {"combatant_%s" % n: get_combatant(battle_infobox_json.get("combatant%s" % n)) for n in range(1, 4)}


def get_combatant(value):
    if not value:
        return []

    wt = mw.parse(value.strip())

    links = wt.filter_wikilinks()
    links_e = [l.__strip__() for l in links if not l.title.startswith(("File:", "Image:"))]
    for l in links:
        wt.remove(l)

    templates = get_templates(wt, ["flagicon", "flagicon image","flagcountry", "flag", "Flagdeco", "flagu", "flagcountry", "Flag icon", "army", "navy"])
    templates_e = [str(i.params[0]) for i in templates]
    for t in templates:
        wt.remove(t)

    non_ref_text = " ".join([str(t) for t in wt.filter(recursive=False, matches=lambda node: not node.startswith(("<ref", )))])

    acronyms = ACRONYMS_PAT.findall(non_ref_text)

    return list(OrderedDict.fromkeys(links_e + templates_e + acronyms))  # Removes duplicates


def get_features(battle_json):
    if not battle_json or battle_json["infobox"].get("error"):
        return {}

    comb_lists = get_combatants(battle_json["infobox"])
    features = dict()
    features.update({COMBATANT_FIRST[i-1]: next(iter(comb_lists.get("combatant_%i" % i)), None) for i in range(1, 4)})
    features.update({COMBATANT_LISTS[i-1]: comb_lists.get("combatant_%i" % i) for i in range(1, 4)})
    return features
