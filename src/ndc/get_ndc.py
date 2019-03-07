import urllib.request
from bs4 import BeautifulSoup
import json


def extract(index):
    url = "http://yozora.main.jp/"

    html = urllib.request.urlopen(url)

    # htmlをBeautifulSoupで扱う
    soup = BeautifulSoup(html, "lxml")

    a_list = soup.find_all(class_="navi")[index].find_all("a")
    arr = []

    for a in a_list:
        id = a.get("href").split(".")[0]
        name = a.text
        print(name)
        print("id\t" + id)

        obj = {}
        obj["name"] = name
        obj["id"] = id
        arr2 = []
        obj["children"] = arr2
        arr.append(obj)

        url2 = "http://yozora.main.jp/" + id + ".html"

        html2 = urllib.request.urlopen(url2)

        # htmlをBeautifulSoupで扱う
        soup2 = BeautifulSoup(html2, "lxml")

        a_list2 = soup2.find(class_="navi").find_all("a")

        for a2 in a_list2:
            id2 = a2.get("href").split(".")[0]
            print("id2\t" + id2)

            obj2 = {}
            obj2["name"] = a2.text
            obj2["id"] = id2
            arr3 = []
            obj2["children"] = arr3
            arr2.append(obj2)

            url3 = "http://yozora.main.jp/" + id2 + ".html"

            html3 = urllib.request.urlopen(url3)

            # htmlをBeautifulSoupで扱う
            soup3 = BeautifulSoup(html3, "lxml")

            a_list3 = soup3.find(class_="navi").find_all("a")

            for a3 in a_list3:
                id3 = a3.get("href").split(".")[0]

                id3 = id2.split("/")[0] + "/" + id3
                print("id3\t" + id3)

                obj3 = {}
                obj3["name"] = a3.text
                obj3["id"] = id3
                obj3["value"] = 0
                arr3.append(obj3)

    return arr


result = {}
result["name"] = "all"
arr = []
result["children"] = arr

arr.append({
    "name": "分野別トップ",
    "children": extract(0)
})

arr.append({
    "name": "児童書トップ",
    "children": extract(1)
})

with open('data/ndc.json', 'w') as outfile:
    json.dump(result, outfile, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
