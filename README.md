# 青空文庫テキストのTEI自動化プロジェクト

[![CC0](http://i.creativecommons.org/p/zero/1.0/88x31.png "CC0")](http://creativecommons.org/publicdomain/zero/1.0/deed.ja)

青空文庫テキストを[Best Practice for TEI in Libraries](http://www.tei-c.org/SIG/Libraries/teiinlibraries/4.0.0/bptl-driver.html)のLevel 2程度の深度で自動的にマークアップしたTEIファイルを格納しています。

**Level 3やLevel 4の深度でマークアップする際の入力ファイルとしてご利用ください。**

参考：[青空文庫テキストをより便利にする（機械可読性を高める）ためのプロジェクト](https://github.com/TEI-EAJ/aozora_tei)

## ディレクトリ構造

TEI/XMLファイルの格納先： docs/data

例： docs/data/000005/files/53194_45356.xml

ディレクトリ構造およびファイル名は[青空文庫のGitHubリポジトリ](https://github.com/aozorabunko/aozorabunko)を参考にしています。

（参考）[青空文庫のHTMLファイルのURLを入力してTEI/XMLファイルを表示する](https://tei-eaj.github.io/auto_aozora_tei/html/)

## 変換方法

[RELAX NG （リラクシング、RELAX Next Generation）](http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng)ファイルを用いてバリデーションを実施しています。


### ヘッダー

[青空文庫テキストをより便利にする（機械可読性を高める）ためのプロジェクト](https://github.com/TEI-EAJ/aozora_tei)で定めた形式に変換しています。

### 本文

上述のスキーマに準拠するように、以下の変換処理を実施しています。

* タグ
    * タグはすべてspanタグに置換し、rendition属性に変換前のタグ情報を与えています。
    * 例：h4   =>   span rendition="h4"

* 属性（置換）
    * 形式的なバリデーションをクリアするための置換処理を含んでいます。
    * したがって、置換後の属性の使用方法の正しさは考慮できていません。

| 変換前 | 変換後 |
----|---- 
| class | rend |
| id | xml:id |
| src | facs |
| alt | source |
| gaiji | change |
| dir | target |
| align | to |
| name | synch |
| href | corresp |

* 属性（削除）

| 属性 | 
----|
| rel | 
| valign | 
| property |
| border |
| cellpadding |
| vto |
| height |
| width | 

## 可視化例

* [作成日/公開日をタイムラインで見る](https://tei-eaj.github.io/auto_aozora_tei/html/timeline.html)
* [入力者/校正者の数を見る](https://tei-eaj.github.io/auto_aozora_tei/html/stats.html)
* （参考）[青空文庫のHTMLファイルのURLを入力してTEI/XMLファイルを表示する](https://tei-eaj.github.io/auto_aozora_tei/html/)