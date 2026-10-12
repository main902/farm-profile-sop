import sys,os
from playwright.sync_api import sync_playwright
page=sys.argv[1]; w=int(sys.argv[2])
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={'width':w,'height':800},device_scale_factor=2 if w<500 else 1)
    pg.goto('file://'+os.path.abspath('../site/'+page)); pg.wait_for_timeout(600)
    pg.add_style_tag(content='.pg-toc{position:static!important}')
    print('sw',pg.evaluate('document.documentElement.scrollWidth'))
    for s in sys.argv[3:]:
        pg.locator('#'+s).screenshot(path=f'../site/{"n" if w<500 else "d"}_{s}.png')
    b.close()
