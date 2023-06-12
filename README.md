# niconico-msky v1.0.0

## niconico-msky is 何
ニコニコ動画に投稿された動画を、Twitter共有ボタンでおなじみの形式でmisskeyに共有するURLを作ってくれます。  
例えば、動画: sm9, サーバー: misskey.okaits7534.mydns.jpで入力すると、次のURLが貰えます。

```
https://misskey.okaits7534.mydns.jp/share?text=%E6%96%B0%E3%83%BB%E8%B1%AA%E8%A1%80%E5%AF%BA%E4%B8%80%E6%97%8F%20-%E7%85%A9%E6%82%A9%E8%A7%A3%E6%94%BE%20-%20%E3%83%AC%E3%83%83%E3%83%84%E3%82%B4%E3%83%BC%EF%BC%81%E9%99%B0%E9%99%BD%E5%B8%AB%0Ahttps%3A//www.nicovideo.jp/watch/sm9%3Fref%3Dmisskey%0A%0A%23sm9%0A%23%E3%83%8B%E3%82%B3%E3%83%8B%E3%82%B3%E5%8B%95%E7%94%BB
```
（出力されたURLのドメイン部分を変えると他のサーバーで流用もできます。）
## 使い方
### 初期設定
Python3の使える環境をセットアップしてください。
#### サーバーの追加
<details><summary>開く</summary>

1. 次のコマンドを実行
   ```bash
   python3 main.py -cu 自分のサーバーのURL
   ```
</details>

#### サーバーの削除
<details><summary>開く</summary>

1. 次のコマンドを実行する
   ```bash
   python3 main.py -du 削除するサーバーのURL
   ```
   または
   ```bash
   python3 main.py -d
   ```
   を実行して、対象のサーバーの番号を入力
</details>

### インタラクティブモード
<details><summary>開く</summary>

1. `python3 main.py -i`  
   (一時的に他のサーバーを指定したい場合、`python3 main.py -iu サーバーのURL`を実行してください。)
2. 複数サーバーが登録されていて、サーバーの指定がない場合:
   1. `Multiple servers found in your config file:`の後に登録されたサーバーの一覧が出てくるので、自分のサーバーの番号を確認
   2. `Which server do you want to use? > `にその番号を入力する
3. `videoid> `と聞かれたら、共有したい動画のIDを入れます
4. こんな感じに確認メッセージが出てくるので、Yを押します （例としてsm9を挙げます）
   ```
   videoid> sm9
   Video informations:
   	Title		: 新・豪血寺一族 -煩悩解放 - レッツゴー！陰陽師
   	URL		: https://www.nicovideo.jp/watch/sm9
   	Contributer	: 中の (4)
   Is it OK? (Y/n)> y
   ```
5. 結果の共有URLが出力されます
6. `Do you want to open it with your default browser? (Y/n)> `にYで答えると、自動的にブラウザでURLを開いてくれます
7. 他に共有したい動画があれば4に戻り、なければ`videoid> `に`exit`と答えることで終了します。
</details>

### 動画ID指定モード
<details><summary>開く</summary>
動画ID指定モードでは、出力がなるべく簡潔になります。

#### 登録されたサーバーが一つ、または登録された全てのサーバーを使う場合
1. `python3 main.py -v 動画ID`
2. 結果の共有URLが出力されます

#### 登録されたサーバーが２つ以上、または一時的に他のサーバーのURLを使う場合
1. `python3 main.py -v 動画ID -u サーバーのURL`
2. 結果の共有URLが出力されます
</details>

### その他オプション
#### server_urlオプション
一時的に他のサーバーを使用したい場合、もしくはサーバー選択画面, サーバー入力画面をスキップしたい場合`-u`または`--server_url`を使用してください。  
（`-t`, `--text`オプションと併用した場合、無視されます。）
#### textオプション
URLではなくただの文字列を取得したい場合、`-t`または`--text`を使用してください。  
（`-v`, `-i`以外のモードの場合、無視されます。）

## ライセンス
MIT Licenseが適用されます。