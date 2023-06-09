# niconico-msky v1.0.0

## niconico-msky is 何
ニコニコ動画に投稿された動画を、Twitter共有ボタンでおなじみの形式でmisskeyに共有するURLを作ってくれます。
例えば、動画: sm9, サーバー: misskey.okaits7534.mydns.jpで入力すると、次のURLが貰えます。

```
https://misskey.okaits7534.mydns.jp/share?text=%E6%96%B0%E3%83%BB%E8%B1%AA%E8%A1%80%E5%AF%BA%E4%B8%80%E6%97%8F%20-%E7%85%A9%E6%82%A9%E8%A7%A3%E6%94%BE%20-%20%E3%83%AC%E3%83%83%E3%83%84%E3%82%B4%E3%83%BC%EF%BC%81%E9%99%B0%E9%99%BD%E5%B8%AB%0Ahttps%3A//www.nicovideo.jp/watch/sm9%3Fref%3Dmisskey%0A%0A%23sm9%0A%23%E3%83%8B%E3%82%B3%E3%83%8B%E3%82%B3%E5%8B%95%E7%94%BB
```
## 使い方
1. Python3を使える環境をセットアップ
2. main.pyを実行します
3. **初回のみ** `Misskey server> `となったら、サーバーのURLを入れます
4. `videoid> `となったら、共有したい動画のIDを入れます
5. こんな感じに確認メッセージが出てくるので、Yを押します （例としてsm9を挙げます）

```
videoid> sm9
Video informations:
	Title		: 新・豪血寺一族 -煩悩解放 - レッツゴー！陰陽師
	URL		: https://www.nicovideo.jp/watch/sm9
	Contributer	: 中の (4)
Is it OK? (y/n)> 
```
1. 結果の共有URLが出力されます
2. `Do you want to open it with your default browser? (Y/n)> `にYで答えると、自動的にブラウザでURLを開いてくれます

## ライセンス
MIT Licenseが適用されます。