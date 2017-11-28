import json
import sys

from utils import process_file_by_line

from features import casualties, combatants, coordinates, country, date, results, strengths


def extract_battle_features(line):
    battle = json.loads(line)

    if battle["infobox"].get("error"):
        return None

    features = dict()
    for module in [combatants, ]:
        features.update(module.get_features(battle))

    features.update(results.get_features(battle, {cl: features.get(cl, []) for cl in combatants.COMBATANT_LISTS}))

    return json.dumps(features) if features else None

if len(sys.argv) != 3:
    print("Incorrect number of argument passed to the job")
    sys.exit(1)

filename_in = sys.argv[1]
filename_out = sys.argv[2]
process_file_by_line(open(filename_in, mode="r"), open(filename_out, mode="w"), extract_battle_features)
