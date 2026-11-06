# キット同梱ガイド：K式ページから「キットが届いてから発送まで」だけを抜き出してA4 PDFに
# 使い方（リポジトリ直下で）: python3 src/mkkitguide.py K式_キット同梱ガイド_A4.pdf
import os,sys
from playwright.sync_api import sync_playwright
HIDE=['s-g4','step1','s-haichi_k','s-fig3a','s-fig3b','step2','step7','s-g5','s-g6','s-g7']
css='''
.pg-toc,.pg-back,.pg-nav,.pg-lead,.pg-cta,.pg-btn,.pg-orig,#xfig2k em.go,.pg-foot{display:none!important}
body{background:#fff!important}
.pg-sec{box-shadow:none!important;border:1px solid #dfe5e1;break-inside:avoid;page-break-inside:avoid;margin:8px auto!important}
.pg-step{break-after:avoid;page-break-after:avoid;margin-top:14px!important}
.pg-top{padding:14px 16px!important}
*{animation:none!important;transition:none!important}
a{color:inherit!important;text-decoration:none!important}
.kitnote{max-width:1040px;margin:10px auto 0;border:2px solid #3f6b45;background:#e8f0e7;border-radius:12px;padding:10px 16px;font-size:17px;line-height:1.6}
'''+''.join('#%s{display:none!important}'%h for h in HIDE)
js='''()=>{
const t=document.querySelector('.pg-top'); const h=t.querySelector('h1'); h.textContent='蓄積型（K式）キット同梱ガイド';
const p=t.querySelector('p'); p.textContent='キットが届いてから、採材・撮影・発送までの手順です。';
const n=document.createElement('div'); n.className='kitnote';
n.innerHTML='<b>このガイドの範囲：</b>STEP 3 キットが届く → STEP 4 採材・撮影 → STEP 5 終わりにする → STEP 6 冷凍便で発送とアップロード<br>申請・Zone登録・結果の見かたは、Webの実施SOP（https://main902.github.io/farm-profile-sop/k-shiki.html）をご覧ください。';
t.after(n);
}'''
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1100,'height':1400})
    pg.goto('file://'+os.path.abspath('k-shiki.html')); pg.wait_for_timeout(800)
    pg.add_style_tag(content=css); pg.evaluate(js)
    pg.pdf(path=sys.argv[1],format='A4',print_background=True,scale=0.66,margin={'top':'8mm','bottom':'8mm','left':'7mm','right':'7mm'},display_header_footer=True,header_template='<span></span>',footer_template='<div style="font-size:8px;width:100%;text-align:center;color:#888">蓄積型（K式）キット同梱ガイド　<span class="pageNumber"></span>/<span class="totalPages"></span>　BRDC Frontiers</div>')
    b.close()
