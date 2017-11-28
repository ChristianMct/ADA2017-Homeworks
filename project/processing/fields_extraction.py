import json
import mwparserfromhell as mwp
import sys

from utils import process_file_by_line


def get_infobox(wikitext):
    ibxs = [t for t in wikitext.filter_templates() if t.name.matches("Infobox military conflict")]
    if len(ibxs) == 0:
        return {"error": "no infobox"}
    if len(ibxs) > 1:
        return {"error": "more than one infobox"}
    return {str(p.name).strip(): str(p.value) for p in ibxs[0].params}


def get_params(template):
    return {str(p.name): p.value.split(",") for p in template.params}


def get_coordinates(wikitext):
    coords = [t for t in wikitext.filter_templates() if t.name.matches("coord")]
    if len(coords) == 1:
        return str(coords[0])

    first_title_coord = str(next(filter(lambda t: "title" in get_params(t).get("display", []), coords), ""))

    first_coord = str(next(iter(coords), ""))

    return first_title_coord if first_title_coord else first_coord if first_coord else None




def extract_battle_infos(page_json):
    battle = json.loads(page_json)
    wikitext = mwp.parse(battle["text"])

    battle["infobox"] = get_infobox(wikitext)
    battle["coordinates"] = get_coordinates(wikitext)  # coordinates are mostly outside of the infobox

    del battle["text"]  # Get rid of the full text
    return json.dumps(battle)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Incorrect number of argument passed to the job")
        sys.exit(1)

    filename_in = sys.argv[1]
    filename_out = sys.argv[2]
    limit = int(sys.argv[3]) if len(sys.argv) >= 4 else None

    process_file_by_line(open(filename_in, mode="r"), open(filename_out, mode="w"), extract_battle_infos, limit)
