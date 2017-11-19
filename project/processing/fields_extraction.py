import json
import mwparserfromhell as mwp
import multiprocessing as mp
import sys


def get_templates(tree, name):
    return [t for t in tree.filter_templates() if t.name.matches(name)]


def get_infobox(wikitext):
    ibxs = get_templates(wikitext, "Infobox military conflict")
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
    return battle


def process_file(file_in, file_out):
    pages = file_in.readlines()
    pages_c = len(pages)
    thread_c = mp.cpu_count()
    pool = mp.Pool(thread_c)
    data = pool.imap_unordered(extract_battle_infos, pages)
    result = list()
    for i, v in enumerate(data, 1):
        sys.stdout.write('\rProcessing %i pages using %i threads... (%i %%)' % (pages_c, thread_c, (i/pages_c)*100))
        result.append(v)
    json.dump(list(result), file_out)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Incorrect number of argument passed to the job")
        sys.exit(1)

    filename_in = sys.argv[1]
    filename_out = sys.argv[2]
    process_file(open(filename_in, mode="r"), open(filename_out, mode="w"))
