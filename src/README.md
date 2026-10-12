# ビルド元（説明ページの生成スクリプト）

- `pages.py` … index.html / odan.html / k-shiki.html を生成（`python3 pages.py` → `../site/` に出力されるので、リポジトリ直下へコピー）
- `fig*.html`, `g*.html`, `p*.html`, `haichi.html`, `o/*.html` … 各図・各セクションの元HTML（PC幅1000px基準）
- `m/*.css` … スマホ（960px以下）用の上書きCSS（図ごと）
- `pg.css`, `pgm.css`, `base.css` … ページ共通CSS
- 出力先ディレクトリ `../site/` と `../site/docs`（PDF）, `../site/img` を用意してから実行
- 表記ルール：正式名「診療・農場フロー蓄積型パッケージ（K式）」はK式ページ題名のみ。目次のフロー箱・カードは「診療・農場フロー／蓄積型（K式）」2行。それ以外は「蓄積型（K式）」。フォームの選択肢は「K式」。
