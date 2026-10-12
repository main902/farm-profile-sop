import sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch()
    for n in sys.argv[1:]:
        pg=b.new_page(viewport={'width':1000,'height':800},device_scale_factor=2)
        pg.goto(f'file://{__import__("os").getcwd()}/{n}.html')
        pg.locator('body > .w').screenshot(path=f'{n}.png')
    b.close()
