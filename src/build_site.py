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
FORM='https://docs.google.com/forms/d/e/1FAIpQLSdV2-E2YteqzdCNkF99YDuRffNlWEpdek1MivJMex-iblThvQ/viewform?usp=dialog'
steps=[(1,'申請フォームで申請','申請','申請のしかたへ'),
(2,'配置図を修正して、Zoneを登録','Zone登録','配置図とZoneの説明へ'),
(3,'キット（コンテナ）が届く','キット','キットの中身へ'),
(4,'期限までに、採材・撮影','採材・撮影','採材と撮影へ'),
(5,'終わりにする（先生が判断）','終わりにする','目安の頭数へ'),
(6,'アップロードと発送','発送','アップロードと発送へ'),
(7,'結果レポートが返ってくる','結果','結果の見かたへ')]
figs=[(0,'fig2k','K式の流れ','各ステップを押すと、その説明へ移動します'),
(1,'g4','申請のしかた','Googleアカウントを用意 → 農場のGoogle Map情報 → 申請フォームで「K式」を選ぶ → 共有フォルダのアドレスがメールで届く'),
(2,'haichi','配置図の修正（記入例）','センターが番号をふった配置図を確認し、表に牛舎の詳細を書きます'),
(2,'fig3a','Zoneとは','牛の段階・収容方法・空間と換気・飼料と哺乳の4つが同じ場所が1つのZone'),
(2,'fig3b','Zoneの登録','分娩60日前からの母牛と、135日齢までの子牛がいる場所を登録'),
(3,'fig4','キットの中身','NPS採取用チューブ25本（色付きキャップ：緑16・橙6・赤3）と白カード5枚'),
(4,'fig5','牛1頭ずつ：個体の撮り方','スマホは縦・1頭1本：チューブ → 胸囲（声）→ Zone名（声）→ 耳標 → 顔 → 横 → 後ろ'),
(4,'fig10','NPSの採り方','下・斜め内側へ入れ、咽頭壁で10回まわす。チューブは立てたまま冷凍庫へ'),
(4,'fig8','Zoneの撮影','時間のあるときに。スマホは横・1Zone 1本・止めずに：カード → Zone全体（消毒槽、水槽・水桶に寄る）→ ＋α'),
(4,'fig9','Zoneカードの例','牛房サイズを書いて、撮るところを番号順に'),
(4,'fig7','農場の聞き取り','時間のあるときに。紙に手書きして写真、またはPDFに直接入力。どちらでもOK'),
(5,'fig11','なぜ、この頭数なの？','目安の数が集まったら、または期限が来たら終わり。NPS（緑・橙）は目標15頭 → 目安8頭以上 → 最低5頭'),
(6,'fig6','共有フォルダとアップロード','アップロードは後日まとめてOK。発送したらセンターにメール。個体の動画は牛の日齢のフォルダへ'),
(7,'g5','プロファイル結果','１か月以内に返送。獣医師向けの「SeF生データ」と、農家さん向けの「SeFレポート」'),
(7,'g6','Add-on解析で「Act」まで','問題が見えたところだけを深く調べ、対策につなげて、効果まで確かめる'),
(7,'g7','Add-on解析　お悩み別メニュー','SeFレポートの提案を見て、センターへメールでご相談ください')]
base=open('base.css').read()
root=re.search(r':root\{[^}]*\}',base).group(0)
mob_generic=open('m/mobile.css').read().replace('width:560px!important','width:100%!important')
desk_css=[];mob_css=[];sections=[];toc=[]
CYC='''<div class="mcyc"><div style="--c:#e0561b">📊 <b>農場プロファイル</b><small>農場全体を広く見る</small></div><i>▼</i><div style="--c:#c28a00;background:#fdf5dc">🔍 <b>Check！</b><small>SeFレポートで問題発見</small></div><i>▼</i><div style="--c:#2f6688;background:#e6eef3">🔬 <b>Add-on解析</b><small>原因を深く調べる</small></div><i>▼</i><div style="--c:#2f7d3a;background:#eaf5eb">🛠️ <b>Act</b><small>対策を決めて実行</small></div><i>▼</i><div style="--c:#6b3fa0">🔁 <b>Re-profile</b><small>対策した段階を測り直す</small></div><i class="up">↺ はじめにもどる</i></div>'''
cur=None
for st,f,title,cap in figs:
    fid='x'+f
    s=open(f+'.html').read()
    st_css=''.join(re.findall(r'<style>(.*?)</style>',s,flags=re.S))
    desk_css.append(scope(base.replace(root,''),fid)); desk_css.append(scope(st_css,fid))
    mc=mob_generic+('\n'+open(f'm/{f}.css').read() if os.path.exists(f'm/{f}.css') else '')
    mob_css.append(scope(mc,fid))
    body=re.search(r'<body>(.*)</body>',s,flags=re.S).group(1)
    if f=='fig2k':
        def rep(m):
            n=int(m.group(2))
            lab=steps[n-1][3]
            return f'<a class="stl" href="#step{n}">'+m.group(0).replace('</small></div></div>',f'</small><em class="go">{lab} ›</em></div></div>')+'</a>'
        body=re.sub(r'<div class="st( \w+)?"><div class="n">(\d)</div><div>.*?</small></div></div>',rep,body)
        body=body.replace('<div class="side">時間のあるときに：Zoneの撮影・聞き取りシート</div>','<div class="side">時間のあるときに：<a href="#s-fig8">Zoneの撮影 ›</a>・<a href="#s-fig7">聞き取りシート ›</a></div>')
    if f=='fig5':
        body=body.replace('<div class="bb">\n <div class="pre">','<div class="bb">\n <div class="pgh">🎬 動画を撮る前に</div>\n <div class="pre"><span class="lab">NPSを採る牛</span>',1)
        body=body.replace(' <div class="pre"><div class="pc" style="border-color:#8a6d00',' <div class="pre p2"><span class="lab">0〜30日齢・胸囲だけの牛</span><div class="pc" style="border-color:#8a6d00',1)
        body=body.replace(' <div class="chain">',' <div class="pgh">📹 動画の中で撮る順番</div>\n <div class="chain">',1)
    if f=='g4':
        body=body.replace('<div class="bot">このあとは、選んだルートのSOPページへ ▶</div>',f'<div class="bot"><a class="pg-btn" href="{FORM}" target="_blank" rel="noopener">📝 申請フォームを開く</a></div>')
    if f=='g6':
        body=body.replace('<svg viewBox="0 0 944 560"',CYC+'<svg class="dcyc" viewBox="0 0 944 560"')
    if st!=cur:
        cur=st
        if st==0:
            toc.append('<a href="#s-fig2k"><span>▶</span>K式の流れ</a>')
        else:
            n,full,short,_=steps[st-1]
            toc.append(f'<a href="#step{n}"><span>{n}</span>{short}</a>')
            sections.append(f'<div class="pg-step" id="step{n}"><span class="pg-no">{n}</span><div><small>STEP {n}</small><b>{full}</b></div></div>')
    tag='' if st==0 else f'<span class="pg-tagst">STEP {st}</span>'
    sections.append(f'<section class="pg-sec" id="s-{f}">{tag}<h2>{title}</h2><p class="pg-cap">{html.escape(cap)}</p><div class="pg-fig" id="{fid}">{body}</div>{"" if st==0 else '<a class="pg-back" href="#s-fig2k">▲ 流れにもどる</a>'}</section>')
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
.pg-sec > h2{{margin:0;font-size:clamp(20px,4vw,26px);font-weight:900;display:flex;align-items:center;gap:10px}}
.pg-step .pg-no{{display:inline-block;min-width:32px;height:32px;border-radius:50%;background:#3f6b45;color:#fff;text-align:center;line-height:32px;font-size:17px}}
.pg-sec .pg-cap{{margin:6px 0 10px;color:#5d6a64;font-size:15px}}
.pg-fig{{overflow:hidden}}
.pg-fig > .w{{margin:0 auto;padding-top:4px!important}}
.pg-fig h1{{display:none!important}}
.pg-back{{display:inline-block;margin-top:10px;font-size:14px;font-weight:700;color:#3f6b45;text-decoration:none;border:1px solid #cfd8d2;border-radius:999px;padding:4px 14px;background:#fafcfa}}
#xfig2k a.stl{{display:block;text-decoration:none;color:inherit;border-radius:14px;transition:transform .12s, box-shadow .12s}}
#xfig2k a.stl:hover .st,#xfig2k a.stl:focus .st{{box-shadow:0 0 0 3px #ffe08a;transform:translateY(-1px)}}
#xfig2k a.stl:active .st{{transform:scale(.99)}}
#xfig2k .go{{display:table;margin-top:5px;font-style:normal;font-size:14px;font-weight:900;color:#fff;background:#3f6b45;border-radius:999px;padding:1px 12px}}
#xfig2k .st.end .go{{background:#c2362b}}
#xfig2k .side a{{color:#5c4900;font-weight:900;text-decoration:underline}}
.pg-step{{max-width:1040px;margin:30px auto 0;display:flex;align-items:center;gap:12px;padding:10px 16px;background:#3f6b45;color:#fff;border-radius:14px;scroll-margin-top:56px}}
.pg-step .pg-no{{display:inline-block;min-width:44px;height:44px;border-radius:50%;background:#fff;color:#3f6b45;text-align:center;line-height:44px;font-size:24px;font-weight:900}}
.pg-step small{{display:block;font-size:13px;font-weight:700;opacity:.85;letter-spacing:.08em}}
.pg-step b{{display:block;font-size:clamp(19px,4vw,24px);font-weight:900;line-height:1.3}}
.pg-tagst{{display:inline-block;font-size:12px;font-weight:900;color:#3f6b45;background:#e8f0e7;border-radius:999px;padding:0 10px;margin-bottom:2px}}
.pg-btn{{display:inline-block;background:#c2362b;color:#fff!important;text-decoration:none;font-weight:900;font-size:18px;border-radius:999px;padding:8px 22px}}
.pg-fig .sh{{display:none!important}}
.pg-fig > .w > .sec{{border:none!important;margin:0!important}}
#xg4 .n{{display:none!important}}
#xg4 .bot{{background:none!important}}
#xg6 .lead{{display:none}}
#xg6 .mcyc{{display:none}}
.mcyc{{flex-direction:column;align-items:stretch;gap:2px;max-width:420px;margin:4px auto}}
.mcyc div{{border:3px solid var(--c);border-radius:12px;padding:6px 12px;font-size:20px;background:#fff}}
.mcyc b{{color:var(--c);font-size:19px}}
.mcyc small{{display:block;font-size:14px;font-weight:700;color:#5d6a64;margin-left:30px}}
.mcyc i{{font-style:normal;text-align:center;color:#f08a3c;font-size:16px;line-height:1.2}}
.mcyc i.up{{font-weight:900;color:#e0561b;font-size:14px}}
.pg-fig .pgh{{font-size:18px;font-weight:900;color:#3f6b45;margin:6px 0 8px;padding-bottom:4px;border-bottom:2px solid #cfe0cf}}
#xfig5 .pre{{border:2px solid #cfd8d2;border-radius:12px;padding:8px 10px;flex-wrap:wrap}}
#xfig5 .pre.p2{{border-color:#e3cf8a;background:#fffcf0}}
#xfig5 .pre .lab{{flex-basis:100%;font-size:15px;font-weight:900;color:#5d6a64}}
.pg-foot{{max-width:1040px;margin:18px auto 40px;padding:0 16px;color:#5d6a64;font-size:13px}}
{''.join(desk_css)}
@media (max-width:{BP}px){{
.pg-sec{{margin:12px 8px;padding:12px 10px 14px;border-radius:12px}}
.pg-top{{padding:18px 14px 14px}}
{''.join(mob_css)}
#xg6 .mcyc{{display:flex}}#xg6 svg.dcyc{{display:none!important}}
.pg-step{{margin:22px 8px 0;padding:8px 12px}}
}}
</style></head><body>
<header class="pg-top"><div class="pg-in"><span class="pg-tag">農場プロファイル</span><h1>診療・農場フロー型パッケージ（K式）実施SOP</h1><p>日々の診療のついでに、期限までに少しずつ。1日でまとめてもOK。</p>
<div class="pg-lead"><a href="#s-fig2k">はじめから見る ▶</a><a href="#step7">📊 結果の見かた</a><a href="K式_実施ガイド_A4印刷用.pdf">🖨 印刷用PDF（A4）</a></div></div></header>
<nav class="pg-toc"><div class="pg-wrap">{''.join(toc)}</div></nav>
{''.join(sections)}
<p class="pg-foot">くわしい手順（詳細SOP）は、農場プロファイル実施SOPのNotionページにあります。　© BRDC Frontiers プロファイルセンター</p>
</body></html>'''
open('../site/k-shiki.html','w').write(page)
print(len(page))
