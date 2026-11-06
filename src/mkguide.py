import os,sys
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/6874ab75-f746-52ea-91fb-a6950bccb889/scratchpad/'
css='''
.pg-toc,.pg-back,.pg-nav,.pg-lead,.pg-cta,.pg-btn,.pg-orig,#xfig2k em.go{display:none!important}
body{background:#fff!important}
.pg-sec{box-shadow:none!important;border:1px solid #dfe5e1;break-inside:avoid;page-break-inside:avoid;margin:8px auto!important}
.pg-step{break-after:avoid;page-break-after:avoid;margin-top:14px!important}
.pg-top{padding:14px 16px!important}
*{animation:none!important;transition:none!important}
a{color:inherit!important;text-decoration:none!important}
'''
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1100,'height':1400})
    pg.goto('file://'+os.path.abspath('k-shiki.html')); pg.wait_for_timeout(800)
    pg.add_style_tag(content=css)
    pg.pdf(path=sys.argv[1],format='A4',print_background=True,scale=0.66,margin={'top':'8mm','bottom':'8mm','left':'7mm','right':'7mm'},display_header_footer=True,header_template='<span></span>',footer_template='<div style="font-size:8px;width:100%;text-align:center;color:#888">蓄積型（K式）実施ガイド　<span class="pageNumber"></span>/<span class="totalPages"></span>　BRDC Frontiers</div>')
    b.close()
