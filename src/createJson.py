import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re
import os
import glob
from lxml import etree
import sys
from io import StringIO
import json

files = glob.glob("../docs/data/*/files/*.xml")

prefix = ".//{http://www.tei-c.org/ns/1.0}"

all = {}

map = {}
map2 = {}
map2["Aozora Transcription"] = {}
map2["Aozora Proofreading"] = {}

for i in range(0, len(files)):

    if i % 100 == 0:
        print(str(i + 1) + "/" + str(len(files)))

    input_path = files[i]

    tree = ET.parse(input_path)
    ET.register_namespace('', "http://www.tei-c.org/ns/1.0")
    root = tree.getroot()

    respStmts = root.findall(prefix + "respStmt")
    for respStmt in respStmts:

        if respStmt.find(prefix + "resp") is not None and respStmt.find(prefix + "name") is not None:

            type = respStmt.find(prefix + "resp").text
            name = respStmt.find(prefix + "name").text

            if type == "TEI Encoding":
                continue

            obj = map2[type]

            if name not in obj:
                obj[name] = 0

            obj[name] = obj[name] + 1

    resps = root.find(prefix + "respStmt")
    for resp in resps:
        if resp.text == "作成":
            date = resp.attrib["when"]

            if date not in map:
                map[date] = 0

            map[date] = map[date] + 1

all["date"] = map
all["persons"] = map2

f = open("../docs/data.json", "w")
json.dump(all, f)
f.close()
