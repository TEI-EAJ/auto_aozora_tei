# 青空文庫テキストのTEI自動化プロジェクト

[![CC0](http://i.creativecommons.org/p/zero/1.0/88x31.png "CC0")](http://creativecommons.org/publicdomain/zero/1.0/deed.ja)

青空文庫テキストを[Best Practice for TEI in Libraries](http://www.tei-c.org/SIG/Libraries/teiinlibraries/4.0.0/bptl-driver.html)のLevel 2程度の深度で自動的にマークアップしたTEIファイルを格納しています。

Level 3やLevel 4の深度でマークアップする際の入力ファイルとしてご利用ください。

参考：[青空文庫テキストをより便利にする（機械可読性を高める）ためのプロジェクト](https://github.com/TEI-EAJ/aozora_tei)

## ディレクトリ構造

[青空文庫のGitHubリポジトリ](https://github.com/aozorabunko/aozorabunko)に基づいています。

## 変換方法

[RELAX NG （リラクシング、RELAX Next Generation）](http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng)でバリデーションを実施しています。


### ヘッダー

[青空文庫テキストをより便利にする（機械可読性を高める）ためのプロジェクト](https://github.com/TEI-EAJ/aozora_tei)で定めた形式に変換しています。

### 本文

上述のスキーマに準拠するように、一時的な対応を含め、以下の置換・変換処理を実施しています。

* タグ
    * タグはすべて<span>タグに置換し、rendition属性に元のタグ情報を与えています。
    * 例：<h4>xxx</h4> => <span rendition="h4">xxx</span>

* 属性（置換）
    * 形式的なバリデーションをクリアする目的での置換処理を含み、置換後の属性の使用方法の正しさは考慮できていません。

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