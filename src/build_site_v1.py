import re,os,html
BP=960
def split_rules(css):
    # returns list of (selector, body) ; handles no nested at-rules
    css=re.sub(r'/\*.*?\*/','',css,flags=re.S)
    out=[];i=0
    while True:
        j=css.find('{',i)
        if j<0:break
        k=css.find('}',j)
        sel=css[i:j].strip(); body=css[j+1:k]
        if sel: out.append((sel,body))
        i=k+1
    return out
def scope(css,fid):
    res=[]
    for sel,body in split_rules(css):
        if sel.startswith('@'): continue
        parts=[]
        for s in sel.split(','):
            s=s.strip()
            if not s: continue
            if s in(':root','html'): continue
            s=re.sub(r'^body\s*>\s*','',s)
            if s=='body': parts.append(f'#{fid}'); continue
            if s=='*': parts.append(f'#{fid} *'); continue
            parts.append(f'#{fid} {s}')
        if parts: res.append(','.join(parts)+'{'+body+'}')
    return '\n'.join(res)
figs=[('fig2k','K式の流れ','申請 → Zone登録 → キット到着 → 期限までに採材・撮影 → 終わりにする → アップロード・冷凍便で発送 → 結果'),
('fig11','なぜ、この頭数なの？','NPS（緑・橙）は目標15頭 → 目安8頭以上 → 最低5頭。中心は31〜90日齢。0〜30日齢は胸囲を5頭'),
('fig3a','Zoneとは','牛の段階・収容方法・空間と換気・飼料と哺乳の4つが同じ場所が1つのZone'),
('fig3b','Zoneの登録','分娩60日前からの母牛と、135日齢までの子牛がいる場所を登録'),
('fig4','キットの中身','NPS採取用チューブ25本（色付きキャップ：緑16・橙6・赤3）と白カード5枚'),
('fig5','牛1頭ずつ：個体の撮り方','スマホは縦・1頭1本：チューブ → 胸囲（声）→ Zone名（声）→ 耳標 → 顔 → 横 → 後ろ'),
('fig10','NPSの採り方','下・斜め内側へ入れ、咽頭壁で10回まわす。チューブは立てたまま冷凍庫へ'),
('fig8','Zoneの撮影','スマホは横・1Zone 1本・止めずに：カード → Zone全体（消毒槽、水槽・水桶に寄る）→ ＋α'),
('fig9','Zoneカードの例','牛房サイズを書いて、撮るところを番号順に'),
('fig7','農場の聞き取り','紙に手書きして写真、またはPDFに直接入力。どちらでもOK'),
('fig6','共有フォルダとアップロード','共有フォルダは1〜5の5つ。個体の動画は牛の日齢のフォルダへ')]
base=open('base.css').read()
root=re.search(r':root\{[^}]*\}',base).group(0)
mob_generic=open('m/mobile.css').read().replace('width:560px!important','width:100%!important')
desk_css=[];mob_css=[];sections=[];toc=[]
for n,(f,title,cap) in enumerate(figs,1):
    fid=f'k{n:02d}'
    s=open(f+'.html').read()
    st=''.join(re.findall(r'<style>(.*?)</style>',s,flags=re.S))
    desk_css.append(scope(base.replace(root,''),fid)); desk_css.append(scope(st,fid))
    mc=mob_generic+('\n'+open(f'm/{f}.css').read() if os.path.exists(f'm/{f}.css') else '')
    mob_css.append(scope(mc,fid))
    body=re.search(r'<body>(.*)</body>',s,flags=re.S).group(1)
    if f=='fig2k':
        links={'1':('https://forms.gle/vr7b8SnN8KoWRgaZ8','申請フォームを開く','_blank'),'2':('#s3','Zoneの説明へ',''),'3':('#s5','キットの中身へ',''),'4':('#s6','採材と撮影へ',''),'5':('#s2','頭数の考え方へ',''),'6':('#s11','アップロードと発送へ','')}
        def rep(m):
            n=m.group(2)
            if n not in links: return m.group(0)
            href,lab,tg=links[n]
            t=f' target="{tg}" rel="noopener"' if tg else ''
            return f'<a class="stl" href="{href}"{t}>'+m.group(0).replace('</small></div></div>',f'</small><em class="go">{lab} ›</em></div></div>')+'</a>'
        body=re.sub(r'<div class="st( \w+)?"><div class="n">(\d)</div><div>.*?</small></div></div>',rep,body)
        body=body.replace('<div class="side">時間のあるときに：Zoneの撮影・聞き取りシート</div>','<div class="side">時間のあるときに：<a href="#s8">Zoneの撮影 ›</a>・<a href="#s10">聞き取りシート ›</a></div>')
        body=body.replace('<div class="sub">','<div class="sub">各ステップを押すと、その説明へ移動します。',1)
    toc.append(f'<a href="#s{n}"><span>{n}</span>{title}</a>')
    sections.append(f'<section class="pg-sec" id="s{n}"><h2><span class="pg-no">{n}</span>{title}</h2><p class="pg-cap">{html.escape(cap)}</p><div class="pg-fig" id="{fid}">{body}</div>{'' if n==1 else '<a class="pg-back" href="#s1">▲ 流れにもどる</a>'}</section>')
page=f'''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>K式 実施SOP｜農場プロファイル</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&display=swap" rel="stylesheet">
<style>
{root}
:root{{--page:#f5f7f5}}
*{{box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{margin:0;background:var(--page);color:var(--ink);font-family:"Noto Sans JP","Noto Sans CJK JP","Hiragino Sans","Yu Gothic",sans-serif;line-height:1.5}}
.pg-top{{background:#3f6b45;color:#fff;padding:22px 16px 18px}}
.pg-top .pg-in,.pg-wrap{{max-width:1040px;margin:0 auto}}
.pg-top .pg-tag{{display:inline-block;background:#fff;color:#3f6b45;font-weight:900;border-radius:999px;padding:0 12px;font-size:14px}}
.pg-top h1{{margin:6px 0 4px;font-size:clamp(24px,5vw,36px);font-weight:900;line-height:1.25}}
.pg-top p{{margin:0;font-size:15px;opacity:.95}}
.pg-lead{{display:flex;gap:10px;flex-wrap:wrap;margin-top:12px}}
.pg-lead a{{background:#fff;color:#3f6b45;text-decoration:none;font-weight:900;border-radius:10px;padding:8px 14px;font-size:15px}}
.pg-toc{{position:sticky;top:0;z-index:5;background:#fff;border-bottom:1px solid #dfe5e1;overflow-x:auto;white-space:nowrap;-webkit-overflow-scrolling:touch}}
.pg-toc .pg-wrap{{display:flex;gap:6px;padding:8px 12px}}
.pg-toc a{{display:inline-flex;align-items:center;gap:6px;text-decoration:none;color:#1c2622;font-size:14px;font-weight:700;border:1px solid #cfd8d2;border-radius:999px;padding:4px 12px 4px 4px;background:#fafcfa}}
.pg-toc a span{{display:inline-block;width:22px;height:22px;border-radius:50%;background:#3f6b45;color:#fff;text-align:center;line-height:22px;font-size:12px}}
.pg-sec{{max-width:1040px;margin:18px auto;background:#fff;border-radius:16px;box-shadow:0 1px 3px rgba(0,0,0,.06);padding:16px 20px 18px;scroll-margin-top:56px}}
.pg-sec h2{{margin:0;font-size:clamp(20px,4vw,26px);font-weight:900;display:flex;align-items:center;gap:10px}}
.pg-sec h2 .pg-no{{display:inline-block;min-width:32px;height:32px;border-radius:50%;background:#3f6b45;color:#fff;text-align:center;line-height:32px;font-size:17px}}
.pg-sec .pg-cap{{margin:6px 0 10px;color:#5d6a64;font-size:15px}}
.pg-fig{{overflow:hidden}}
.pg-fig > .w{{margin:0 auto;padding-top:4px!important}}
.pg-fig h1{{display:none!important}}
.pg-back{{display:inline-block;margin-top:10px;font-size:14px;font-weight:700;color:#3f6b45;text-decoration:none;border:1px solid #cfd8d2;border-radius:999px;padding:4px 14px;background:#fafcfa}}
#k01 a.stl{{display:block;text-decoration:none;color:inherit;border-radius:14px;transition:transform .12s, box-shadow .12s}}
#k01 a.stl:hover .st,#k01 a.stl:focus .st{{box-shadow:0 0 0 3px #ffe08a;transform:translateY(-1px)}}
#k01 a.stl:active .st{{transform:scale(.99)}}
#k01 .go{{display:table;margin-top:5px;font-style:normal;font-size:14px;font-weight:900;color:#fff;background:#3f6b45;border-radius:999px;padding:1px 12px}}
#k01 .st.end .go{{background:#c2362b}}
#k01 .side a{{color:#5c4900;font-weight:900;text-decoration:underline}}
.pg-foot{{max-width:1040px;margin:18px auto 40px;padding:0 16px;color:#5d6a64;font-size:13px}}
{''.join(desk_css)}
@media (max-width:{BP}px){{
.pg-sec{{margin:12px 8px;padding:12px 10px 14px;border-radius:12px}}
.pg-top{{padding:18px 14px 14px}}
{''.join(mob_css)}
}}
</style></head><body>
<header class="pg-top"><div class="pg-in"><span class="pg-tag">農場プロファイル</span><h1>診療・農場フロー型パッケージ（K式）実施SOP</h1><p>日々の診療のついでに、期限までに少しずつ。1日でまとめてもOK。</p>
<div class="pg-lead"><a href="#s1">はじめから見る ▶</a><a href="K式_実施ガイド_A4印刷用.pdf">🖨 印刷用PDF（A4）</a></div></div></header>
<nav class="pg-toc"><div class="pg-wrap">{''.join(toc)}</div></nav>
{''.join(sections)}
<p class="pg-foot">くわしい手順（詳細SOP）は、農場プロファイル実施SOPのNotionページにあります。　© BRDC Frontiers プロファイルセンター</p>
</body></html>'''
open('../site/k-shiki.html','w').write(page)
print(len(page))
