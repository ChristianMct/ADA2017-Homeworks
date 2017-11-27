import mwparserfromhell as mw
import re
import difflib as dl
import operator

RESULT_QUALIFIERS = ("decisive", "major", "crushing", "tactical", "tactically", "strategic", "strategically", "pyrrhic")

RESULT_QUALIFIERS_EQUIV = {"tactically": "tactical", "strategically": "strategic"}

RESULT_QUALIFIERS_P = re.compile(r"\b({})\b".format("|".join(RESULT_QUALIFIERS)), re.IGNORECASE)

RESULT_TYPES = ("victory", "defeat", "retreat", "indecisive", "inconclusive", "ceasefire")

RESULT_TYPES_P = re.compile(r"\b({})\b".format("|".join(RESULT_TYPES)), re.IGNORECASE)


def get_results(value, combatants):
    if not value or not value["infobox"].get("result"):
        return []

    wt = mw.parse(value["infobox"].get("result").strip())

    for ref in wt.filter(matches=lambda n: n.startswith(("<ref",))):
        wt.remove(ref)

    wt_str = str(wt)
    for sep in ["<br>", "<br />", "<br/>", "\n"]:
        wt_str = wt_str.replace(sep, ";")

    wt = mw.parse(wt_str)

    return list(filter(lambda x: x, [get_result(line, combatants) for line in wt.strip_code().split(";")]))


def get_result(value, combatants):

    res_types = RESULT_TYPES_P.findall(value)
    if not res_types:
        return
    res_type = res_types[0].lower()  # assumes only one type per line, mostly the case
    if res_type == "inconclusive":
        res_type = "indecisive"
    rest = RESULT_TYPES_P.sub("", value)

    qualifiers = [RESULT_QUALIFIERS_EQUIV.get(qual.lower(), qual.lower()) for qual in RESULT_QUALIFIERS_P.findall(rest)]
    rest = RESULT_QUALIFIERS_P.sub("", rest).strip()

    attribution = argmax(get_attrib_score(rest, combatants))

    return {
        "type": res_type,
        "qualifiers": qualifiers,
        "attribution": attribution if res_type not in ["indecisive", "ceasefire"] else None,
    }


def argmax(dic):
    return max(dic.items(), key=operator.itemgetter(1))[0]


def get_attrib_score(result, combatants):
    def score(comb_names):
        if not comb_names:
            return 0.0
        return max([dl.SequenceMatcher(None, comb_name, result).ratio() for comb_name in comb_names])
    return {comb: score(comb_names) for comb, comb_names in combatants.items()}


def render_result_for_comb(results, combatant):
    return "+".join([" ".join(list(sorted(res["qualifiers"])) + [res["type"]])
                     for res in results if res["attribution"] == combatant])


def results_dicts_to_features(results):
    return {
        "indecisive": "indecisive" in [res["type"] for res in results],
        "tactical_indecisive":  "indecisive" in [res["type"] for res in results if "tactical" in res["qualifiers"]],
        "strategic_indecisive":  "indecisive" in [res["type"] for res in results if "strategic" in res["qualifiers"]],
        "result_combatant_1": render_result_for_comb(results, "combatant_1"),
        "result_combatant_2": render_result_for_comb(results, "combatant_2"),
        "result_combatant_3": render_result_for_comb(results, "combatant_3"),
    }


def get_features(value, combatants):
    results =  get_results(value, combatants)

    return results_dicts_to_features(results)
