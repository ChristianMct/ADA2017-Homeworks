import mwparserfromhell as mw
import re
from utils import get_templates
from collections import OrderedDict

ACRONYMS_PAT = re.compile("\b(?:[A-Z]\.?){2,}")


def get_combatants(value):
    if not value or value["infobox"].get("error"):
        return {}
    return {"combatant_%s" % n: get_combatant(value["infobox"].get("combatant%s" % n)) for n in range(1, 4)}


def get_combatant(value):
    if not value:
        return

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
