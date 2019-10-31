import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re
import os
import glob
from lxml import etree
import sys
from io import StringIO

start = 0

skip_flg = True

template_path = "data/template.xml"

input_dir = "/Users/nakamura/git/aozora/aozorabunko/cards"
output_top_dir = "../docs/data"
files = glob.glob(input_dir + "/*/files/*.html")

# 例外のファイル群
arr_exc = ["2715_28479.xml", "2014_6883.xml", "54694_52028.xml"]

# validation用のリナクシングファイル
rnc_path = "data/tei_all.rng"

# ---------

prefix = ".//{http://www.tei-c.org/ns/1.0}"

# date 2715_28479.xml, 2014_6883.xml
# date yyy nnn dd 54694_52028.xml

# リナクシングファイルの読み込み
with open(rnc_path) as f:
    relaxng_doc = etree.parse(f)
relaxng = etree.RelaxNG(relaxng_doc)


# ルビを変換するメソッド
def convert_ruby(text):
    arr = ["rb", "rt", "rp", "ruby"]

    # 正規表現による置換
    for e in arr:
        text = re.sub('<' + e + '>(.+?)<\/' + e + '>',
                      '<seg type="' + e + '">\\1</seg>', text)

    # 正規表現では対処できなかった場合の置換
    for e in arr:
        text = text.replace("<" + e + ">", "<seg type='" + e + "'>")
        text = text.replace("</" + e + ">", "</seg>")

    return text


def convert(text):
    text = convert_ruby(text)

    # 単純な置換
    text = text.replace(" class=", " rend=")
    text = text.replace("<br/>", "<lb/>")
    text = text.replace("<br />", "<lb/>")
    text = text.replace("<hr/>", "<lb/>")
    text = text.replace("<hr />", "<lb/>")
    text = text.replace(" id=", " xml:id=")
    text = text.replace(" src=", " facs=")
    text = text.replace(" alt=", " source=")
    text = text.replace(" gaiji=", " change=")
    text = text.replace(" dir=", " style=")
    text = text.replace(" target=", " met=")
    text = text.replace(" align=", " to=")
    text = text.replace(" name=", " synch=")
    text = text.replace(" href=", " corresp=")
    text = text.replace(' rel="license"', " ")

    # imgタグの置換
    text = re.sub('<img(.+?)\/>', '<seg rendition="img"\\1></seg>', text)

    # 削除対象の属性の配列
    arr4 = ["valign", "rel", "property", "border",
            "cellpadding", "to", "vto", "height", "width"]
    for e in arr4:
        text = re.sub(' ' + e + '="(.*?)"', ' ', text)

    # hタグの置換
    text = re.sub('<h\d(.+?)<\/h\d>', '<seg rendition="h"\\1</seg>', text)

    # 置換対象のタグの配列（上の処理でh4など消えるはずだが、うまくいかない場合あり）
    arr = ["h5", "h4", "h3", "h2", "h1", "a", "sup", "em", "strong", "ul", "li", "big", "table", "tr", "th",
           "td", "center", "div", "span"]
    for e in arr:
        # 正規表現による置換
        text = re.sub('<' + e + '(.+?)<\/' + e + '>',
                      '<seg rendition="' + e + '"\\1</seg>', text)

        # 正規表現では対処できなかった場合の置換
        text = text.replace("<" + e + "", "<seg rendition='" + e + "'")
        text = text.replace("</" + e + ">", "</seg>")

    # 置換対象の属性なしのタグの配列
    arr3 = ["d", "p", "b", "i", "small"]
    for e in arr3:
        text = re.sub('<' + e + '>(.+?)<\/' + e + '>',
                      '<seg rendition="' + e + '">\\1</seg>', text)
        text = text.replace("<"+e+">", "<seg rendition='" + e + "'>")
        text = text.replace("</" + e + ">", "</seg>")

    # その他の置換対象の配列
    arr2 = ["small", "a", "sub"]
    for e in arr2:
        text = re.sub('<' + e + '(.+?)<\/' + e + '>',
                      '<seg rendition="' + e + '"\\1</seg>', text)

    return text


# 工作員に関する情報を取得するメソッド
def get_dates_and_persons(text):
    # 修正作業用の辞書
    p_types = [{"ja": "入力", "en": "Aozora Transcription"},
               {"ja": "校正", "en": "Aozora Proofreading"}]
    d_types = ["作成", "修正", "公開"]

    dates = []
    persons = []

    lines = text.split("<lb/>")

    for line in lines:
        line = line.strip()

        for type in p_types:
            if line.startswith(type["ja"] + "："):
                person = line.split("：")[1]
                persons.append(
                    {"type@ja": type["ja"], "name": person, "type@en": type["en"]})

        for type in d_types:
            if line.endswith("日" + type):
                date_arr = line.replace(
                    "年", "-").replace("月", "-").replace("日", "-").split("-")
                year = date_arr[0]
                month = date_arr[1].zfill(2)
                day = date_arr[2].zfill(2)

                date = year + "-" + month + "-" + day
                date_str = line.split("日")[0] + "日"

                dates.append({"org": date_str, "rep": date, "type": type})

    return dates, persons


# ヘッダー部分を作るためのメソッド
def handle_bibliographical_information(text):
    text = text.split("<hr/>")[1]

    key = "ボランティアの皆さんです。"

    if len(text.split(key)) > 1:
        text = text.split(key)[0] + key
        text = re.sub('<a href="(.+?)">(.+?)</a>', '\\2', text)
    else:
        text = text.replace("</div>", "")

    # 置換
    text = convert(text)

    # 工作員情報の取得
    dates, persons = get_dates_and_persons(text)

    note = '<note>%s</note>' % text

    return note, dates, persons


count = 0

for i in range(start, len(files)):

    input_path = files[i]

    output_dir = input_path.replace(
        input_dir, output_top_dir).split("files/")[0] + "files"
    output_filename = input_path.split("/")[-1].replace(".html", ".xml")
    output_path = output_dir + "/" + output_filename

    if "_" not in output_filename:
        continue

    if i % 100 == 0:
        print(str(i + 1) + "/" + str(len(files)) + "\t" + input_path)

    # arr10 = ["45210_24671.xml", "47177_37073.xml", "18361_32671.xml", "1745_16941.xml", "47850_31638.xml"]
    arr10 = ["1745_16941.xml"]

    if output_filename in arr10:
        continue

    if skip_flg:

        if os.path.exists(output_path):
            continue

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    tree = ET.parse(template_path)
    ET.register_namespace('', "http://www.tei-c.org/ns/1.0")
    root = tree.getroot()

    f = open(input_path, encoding="sjis", errors='ignore')
    html = f.read()
    f.close()

    soup = BeautifulSoup(html, "lxml")

    bib_infos = soup.select(".bibliographical_information")

    # ヘッダーがないものはスキップ
    if len(bib_infos) == 0:

        count = count + 1

        print("**** non header ****\t" + output_path)
        # continue
        
        respStmt = root.find(prefix + "respStmt")
        if respStmt.find(prefix + "resp") == None:
            respStmt.append(ET.fromstring('<resp/>'))

    else:
        bib_info = bib_infos[0]

        # 文字列解析により、noteの整形、および日時情報、人物情報を取得する
        note, dates, persons = handle_bibliographical_information(
            str(bib_info))

        respStmt = root.find(prefix + "respStmt")

        # 取得した日時情報で、note内の日時情報を書き換える
        for date in dates:
            note = note.replace(
                date["org"], '<date when="%s">%s</date>' % (date["rep"], date["org"]))

            if date["type"] == "作成" or date["type"] == "公開":
                respStmt.append(ET.fromstring(
                    '<resp when="%s">作成</resp>' % date["rep"]))

        if respStmt.find(prefix + "resp") == None:
            respStmt.append(ET.fromstring('<resp/>'))

        try:
            respStmt.append(ET.fromstring(note))
        except:
            print("**** note ****\t" + output_path)
            print(note)

            if output_filename not in arr_exc:
                sys.exit(output_path)

        # 人物情報の追加
        titleStmt = root.find(prefix + "titleStmt")
        for person in persons:
            titleStmt.append(
                ET.fromstring('<respStmt><resp>%s</resp><name>%s</name></respStmt>' % (person["type@en"], person["name"])))

        titleStmt.append(
            ET.fromstring('<respStmt><resp when="2019-01-01">TEI Encoding</resp><name>Input Your Name</name></respStmt>'))

        # タイトルと著者情報の追加
        bibl = root.find(prefix + "bibl")
        bibl.text = "Input by your self"

        t_arr = soup.select(".title")
        if len(t_arr) > 0:
            title = t_arr[0].text
            root.find(prefix + "title").text = title
            bibl.append(ET.fromstring('<title>%s</title>' % title))

        a_arr = soup.select(".author")
        if len(a_arr) > 0:
            author = a_arr[0].text
            root.find(prefix + "author").text = author
            bibl.append(ET.fromstring('<author>%s</author>' % author))

    # ----------- 以下、本文 -----------

    body = root.find(prefix + "body")

    p = ET.Element("{http://www.tei-c.org/ns/1.0}p")
    body.append(p)

    main_texts = soup.select(".main_text")

    # main_textがないものはスキップ
    if len(main_texts) == 0:
        print("**** none main text ****\t" + output_path)
        # continue
        print(input_path)
        break
    else:
        main_text = main_texts[0]

        text = str(main_text)

        text = convert(text)

        try:
            p.append(ET.fromstring(text))
        except:
            print("**** textがおかしい ****\t" + output_path)
            # print(text)
            with open("data/tmp.txt", mode='w') as f:
                f.write(text)
            sys.exit(output_path)

    # --以下、出力 --

    tree.write(output_path, encoding="utf-8")

    # --以下、validation --

    f = open(output_path)
    data = f.read()  # ファイル終端まで全て読んだデータを返す
    f.close()

    valid = StringIO(data)

    doc = etree.parse(valid)

    if not relaxng.validate(doc):
        print("**** validation error ****\t" + output_path)

        if output_filename not in arr_exc:
            sys.exit(output_path)


print(count)
