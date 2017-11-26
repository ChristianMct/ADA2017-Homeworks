import mwparserfromhell as mw
from utils import get_templates


def get_combatants(infobox):
    return {"combatant_%s" % n: get_combatant(infobox.get("combatant%s" % n)) for n in range(1, 4)}


def get_combatant(value):
    if not value:
        return

    wt = mw.parse(value.strip())

    links = [(l, l.title.startswith(("File:", "Image:"))) for l in wt.filter_wikilinks()]
    if links:
        return [str(l.text) if l.text else str(l.title) for l, isImage in links if not isImage]

    flagicons = get_templates(wt, ["flagicon", "flagicon image","flagcountry", "flag", "Flagdeco", "flagu", "flagcountry", "Flag icon", "army", "navy"])
    if flagicons:
        return [str(i.params[0]) for i in flagicons]

    if len(wt.filter()) == 1:
        return [wt.strip_code()]

    return
