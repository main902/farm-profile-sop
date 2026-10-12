import sys,os
from playwright.sync_api import sync_playwright
css=open('m/mobile.css').read()
with sync_playwright() as p:
    b=p.chromium.launch()
    for n in sys.argv[1:]:
        pg=b.new_page(viewport={'width':560,'height':800},device_scale_factor=2)
        pg.goto(f'file://{os.getcwd()}/{n}.html')
        pg.add_style_tag(content=css)
        if os.path.exists(f'm/{n}.css'): pg.add_style_tag(content=open(f'm/{n}.css').read())
        pg.locator('body > .w').screenshot(path=f'm/{n}.png')
    b.close()
