# asannokaikamado.github.io

阿讃の会かまど（上板町の宅配お弁当屋さん）のホームページです。
公開URL：https://asannokaikamado.github.io/

## フォルダ構成

```
index.html              トップページ（1ページ構成）
css/style.css           デザイン（色・フォントは先頭の :root でまとめて変更可）
js/main.js              スマホメニュー・お弁当のカルーセル
tools/update_gallery.py img/menu の写真からカルーセルを作り直すスクリプト
img/
├── 今月の献立.JPG       毎月差し替える献立表（場所・ファイル名は変えない）
├── menu/               カルーセルのお弁当写真
├── menu_old/           以前のお弁当写真（保管用。backup の案A/Cが参照）
├── kondate_old/        過去の献立表（今月の献立(YYYYMM).JPG）
├── logo/               ロゴ・ファビコン（original/ に加工前の元画像）
└── sns/                LINEのQRコード、SNS共有用の画像（ogp.jpg）
backup/                 採用しなかったデザイン案（検索には出ない設定）
THIRD_PARTY_NOTICES.md  使っているアイコン・フォントのライセンス
```

## 毎月の献立表の更新

1. 今の `img/今月の献立.JPG` を `img/kondate_old/今月の献立(YYYYMM).JPG` に移す（例：`今月の献立(202610).JPG`）
2. 新しい献立表を `img/今月の献立.JPG` という名前で置く

HTMLの変更は不要です。拡張子が小文字の `今月の献立.jpg` で置いてしまっても表示されるようにしてありますが、なるべく `.JPG` にそろえてください。

## お弁当の写真を追加する

1. 写真を `img/menu/` に入れる（ファイル名は下のルール）
2. リポジトリのフォルダで次を実行する

   ```
   python tools/update_gallery.py
   ```

   `index.html` のカルーセル部分（`<!-- gallery:start -->` 〜 `<!-- gallery:end -->`）が、`img/menu/` の写真から作り直されます。料理名・サイズの印・画像の説明（alt）・サイズ指定も自動で入ります。
3. 写真を消したとき・名前を変えたときも、同じように実行します

並び順は料理名の順（同じ料理は S → M）です。

### 写真のファイル名のルール

- `料理名(S).jpg` ／ `料理名(M).jpg` … カードに「Sサイズ」「Mサイズ」の印が付きます
- `料理名.jpg` … サイズの印なし
- ファイル名の料理名が、そのままカルーセルに表示されます
- 例：`天ぷら(S).jpg`、`天ぷら(M).jpg`、`ちらし寿司.jpg`

トップの丸い写真3枚（`３色丼(M).jpg`、`ちらし寿司.jpg`、`天ぷら(S).jpg`）は `index.html` に直接書いてあります。この3枚の名前を変えたり消したりするときは、`index.html` の `hero-visual` の部分も直してください。
