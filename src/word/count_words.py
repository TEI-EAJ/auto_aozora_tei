import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re
import os
import glob
from lxml import etree
import sys
from io import StringIO
import json
from rdflib import URIRef, BNode, Literal
from rdflib import Graph

g = Graph()

files = glob.glob("../../docs/data/*/files/*.xml")

prefix = ".//{http://www.tei-c.org/ns/1.0}"

for i in range(0, len(files)):

    if i % 100 == 0:
        print(str(i + 1) + "/" + str(len(files)))

    input_path = files[i]

    p_arr = input_path.split("/")
    creator_id = p_arr[4]
    card_id = p_arr[6].split("_")[0]

    uri = "http://www.aozora.gr.jp/cards/" + creator_id + "/card" + card_id + ".html"

    tree = ET.parse(input_path)
    ET.register_namespace('', "http://www.tei-c.org/ns/1.0")
    root = tree.getroot()

    text = root.find(prefix + "text")
    text = ET.tostring(text, encoding='utf8', method='xml')
    soup = BeautifulSoup(text, features="lxml")

    text = soup.get_text()

    text = text.strip()

    words = len(text)

    if words > 0:
        g.add((URIRef(uri), URIRef("http://purl.org/dc/terms/extent"), Literal(words)))

g.serialize(format='pretty-xml', destination="words.rdf")
