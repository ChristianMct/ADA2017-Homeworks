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


def extract_battle_infos(page_json):
    battle = json.loads(page_json)
    wikitext = mwp.parse(battle["text"])

    battle["infobox"] = get_infobox(wikitext)

    del battle["text"]  # Get rid of the full text
    return json.dumps(battle)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Incorrect number of argument passed to the job")
        sys.exit(1)

    filename_in = sys.argv[1]
    filename_out = sys.argv[2]
    process_file_by_line(open(filename_in, mode="r"), open(filename_out, mode="w"), extract_battle_infos)
