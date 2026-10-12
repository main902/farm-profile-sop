import sys,os
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={'width':375,'height':800},device_scale_factor=2)
    pg.goto('file://'+os.path.abspath('../site/k-shiki.html')); pg.wait_for_timeout(400)
    pg.add_style_tag(content='.pg-toc{position:static!important}')
    print('sw',pg.evaluate('document.documentElement.scrollWidth'))
    for s in sys.argv[1:]:
        pg.locator('#'+s).screenshot(path=f'../site/n_{s}.png')
    b.close()
