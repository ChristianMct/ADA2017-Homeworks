import json
import mwparserfromhell as mwp
import multiprocessing as mp
import sys
import csv

def csv_write(features, values):
    with open(filename_counts, 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
        spamwriter.writerow(features)
        spamwriter.writerow(values)

def get_infobox_counts(infobox, feature):
    errorText = infobox.get('error')
    target = "no infobox"
    if feature == 'infobox_0':
        target = "more than one infobox"
    if errorText is not None:
        if errorText == target:
            return {feature : 'error'}, 1
        else:
            return {feature : 'error'}, 0
    else:
            return {feature : 'ok'}, 0

def get_single_feature(infobox, feature):
    if (feature == 'infobox_0') | (feature =='infobox_1'):
            return get_infobox_counts(infobox.get('infobox'), feature)
    try:
        value_level1 = infobox.get(feature)
        if value_level1 is None:
            value_level2 = infobox.get('infobox')
            if value_level2 is not None:
                return get_single_feature(value_level2, feature)
            else:
                return {feature : 'error'}, 0
        else:
            return {feature : value_level1}, 1 
    except ValueError:
        return {feature : 'error'}, 0
    

def get_features(infobox):
    strResponse = ''
    counts = list()
    for v in features:
        value, count = get_single_feature(infobox, v)
        strResponse = strResponse + ", " + str(value)
        counts.append(count)
    return strResponse, counts 


def extract_infobox_infos(page_json):
    infoboxes = json.loads(page_json)
    infoboxes_c = len(infoboxes)
    thread_c = mp.cpu_count()
    pool = mp.Pool(thread_c)
    data = pool.imap_unordered(get_features, infoboxes)
    result = list()
    present = []
    for i, v in enumerate(data, 1):
        sys.stdout.write('\rProcessing %i pages using %i threads... (%i %%)' % (infoboxes_c, thread_c, (i/infoboxes_c)*100))
        result.append(v[0])
        if i == 1:
            present = v[1]
        else:
            present = [x + y for x, y in zip(present, v[1])]
    print()
    print(features)
    print(present)
    csv_write(features, present)
    return result
    
    

def process_file(file_in, file_out):
    pages = file_in.readlines()
    pages_c = len(pages)
    data = list()
    for v in pages:
        data.append(extract_infobox_infos(v))
    json.dump(list(data), file_out)


if __name__ == "__main__":
    print("running")
    length = len(sys.argv)
    if len(sys.argv) < 4:
        print("Incorrect number of argument passed to the job")
        sys.exit(1)
        
    
    filename_in = sys.argv[1]
    filename_out = sys.argv[2]
    filename_counts = sys.argv[3]
    
    features = []
    for i in range(4,length):
        features.append(sys.argv[i])
    
    process_file(open(filename_in, mode="r"), open(filename_out, mode="w"))