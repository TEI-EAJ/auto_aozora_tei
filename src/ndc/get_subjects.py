import json
from SPARQLWrapper import SPARQLWrapper

sparql = SPARQLWrapper(endpoint='https://dydra.com/ut-digital-archives/aozora/sparql', returnFormat='json')
sparql.setQuery("""
    SELECT DISTINCT (count(?s) as ?c) ?subject WHERE {
    ?s <http://purl.org/dc/elements/1.1/subject> ?subject .
    } group by ?subject
""")
results = sparql.query().convert()

map = {}

for obj in results["results"]["bindings"]:
    print(obj)

    c = int(obj["c"]["value"])
    subjects = obj["subject"]["value"].split(" ")
    for subject in subjects:
        if subject == "NDC":
            continue

        if subject not in map:
            map[subject] = 0

        map[subject] = map[subject] + c

        if "K" in subject:

            subject = subject.replace("K", "")

            if subject not in map:
                map[subject] = 0

            map[subject] = map[subject] + c

fw = open("data/subjects.json", 'w')
json.dump(map, fw, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
