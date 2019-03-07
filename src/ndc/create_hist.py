import urllib.request
from bs4 import BeautifulSoup
import json

with open('data/ndc.json', 'r') as f:
    data = json.load(f)

with open('data/subjects.json', 'r') as f:
    subjects = json.load(f)

arr = data["children"]

for lev1 in arr:

    for lev2 in lev1["children"]:

        for lev3 in lev2["children"]:
            id = lev3["id"]
            id = id.split("/")[-1].replace("ndc", "")

            if id in subjects:
                lev3["value"] = subjects[id]

with open('../../docs/ndc/hist.json', 'w') as outfile:
    json.dump(data, outfile, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
