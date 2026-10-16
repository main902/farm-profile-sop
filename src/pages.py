import re, os, html
os.chdir(os.path.dirname(os.path.abspath(__file__)))
BP = 960
FORM = 'https://docs.google.com/forms/d/e/1FAIpQLSdV2-E2YteqzdCNkF99YDuRffNlWEpdek1MivJMex-iblThvQ/viewform?usp=dialog'
NOTION = {
    '@NOTION_TOP@': 'https://www.notion.so/2b10b8956056814e875ddb38864610da',
    '@NOTION_ODAN@': 'https://www.notion.so/3f40b8956056810fb13fd7915db612ed',
    '@NOTION_K@': 'https://www.notion.so/3f40b8956056810db0e4e74872b8413f',
    '@NOTION_ITEMS@': 'https://www.notion.so/2b10b895605681329daef6db4baa827b',
    '@NOTION_VIDEO@': 'https://www.notion.so/3f40b89560568088acbbee4978316247',
    '@NOTION_MANGA@': 'https://www.notion.so/3f40b89560568023b745f3cdfbc95b29',
}
base = open('base.css').read()
ROOT = re.search(r':root\{[^}]*\}', base).group(0)
PGCSS = open('pg.css').read()
PGM = open('pgm.css').read()
MOBG = open('m/mobile.css').read().replace('width:560px!important', 'width:100%!important')


def split_rules(css):
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    out = []; i = 0
    while True:
        j = css.find('{', i)
        if j < 0: break
        k = css.find('}', j)
        sel = css[i:j].strip(); body = css[j + 1:k]
        if sel: out.append((sel, body))
        i = k + 1
    return out


def scope(css, fid):
    res = []
    for sel, body in split_rules(css):
        if sel.startswith('@'): continue
        parts = []
        for s in sel.split(','):
            s = s.strip()
            if not s: continue
            if s == 'html': continue
            if s == ':root': parts.append(f'#{fid}'); continue
            s = re.sub(r'^body\s*>\s*', '', s)
            if s == 'body': parts.append(f'#{fid}'); continue
            if s == '*': parts.append(f'#{fid} *'); continue
            parts.append(f'#{fid} {s}')
        if parts: res.append(','.join(parts) + '{' + body + '}')
    return '\n'.join(res)


def load(f):
    p = f + '.html' if os.path.exists(f + '.html') else f'o/{f}.html'
    return open(p).read()


SOFT = {
 '#c8361c':'#b4594b','#e0561b':'#cf7c4e','#2f7d3a':'#4e8a5c','#2e8b57':'#5b9a76','#3f6b45':'#56795c',
 '#c2362b':'#b55a4f','#f6a04d':'#efb486','#f08a3c':'#eaa676','#d9822b':'#d39c66','#6b3fa0':'#7d67a2',
 '#8a6d00':'#987f43','#2f6688':'#4f7a95','#f2c14e':'#efd08e','#e57a5c':'#e09c86','#c4302b':'#b55a4f',
 '#c28a00':'#b4944f','#1d6f42':'#3f7d5a','#f3c7a8':'#efd9c8','#ffe08a':'#f3e2ad','#5c4900':'#6a5a2c',
 '#5a4500':'#665632','#f1b9a6':'#ecd0c5','#a9d3ae':'#bcd8bf','#7a5230':'#7f6248','#b0582a':'#ad7556',
 '#c8361c33':'#b4594b33','#e9a59f':'#e6c0bb','#d7261e':'#c0584d','#e98a5f':'#e5a585','#f6c84c':'#efd08e',
 '#5aa864':'#79b07f','#e0561b33':'#cf7c4e33'}
def soften(s):
    import re as _re
    return _re.sub(r'#[0-9a-fA-F]{6}\b', lambda m: SOFT.get(m.group(0).lower(), m.group(0)), s)

def render(cfg):
    desk, mob, sections, toc = [], [], [], []
    cur = None
    first = False
    T = cfg.get('tf', {})
    for it in cfg['items']:
        if it[0] == 'step':
            _, n, full, short = it
            toc.append(f'<a href="#step{n}"><span>{n}</span>{short}</a>')
            sections.append(f'<div class="pg-step" id="step{n}"><span class="pg-no">{n}</span><div><small>STEP {n}</small><b>{full}</b></div></div>')
            cur = n
            first = True
            continue
        if it[0] == 'band':  # unnumbered band
            _, bid, title, short, mark = it
            toc.append(f'<a href="#{bid}"><span>{mark}</span>{short}</a>')
            sections.append(f'<div class="pg-step pg-band" id="{bid}"><span class="pg-no">{mark}</span><div><b>{title}</b></div></div>')
            cur = None
            continue
        # ('sec', sid, title, cap, figs, opts)
        _, sid, title, cap, figs, opts = it
        if opts.get('toc'):
            lab, mark = opts['toc']
            toc.append(f'<a href="#{sid}"><span>{mark}</span>{lab}</a>')
        figs_html = ''
        for fs in figs:
            f, mode = (fs if isinstance(fs, tuple) else (fs, ''))
            fid = 'x' + f
            s = load(f)
            st = ''.join(re.findall(r'<style>(.*?)</style>', s, flags=re.S))
            if 'base.css' in s:
                desk.append(scope(base.replace(ROOT, ''), fid))
            desk.append(scope(st, fid))
            mc = MOBG + ('\n' + open(f'm/{f}.css').read() if os.path.exists(f'm/{f}.css') else '')
            mob.append(scope(mc, fid))
            body = re.search(r'<body>(.*)</body>', s, flags=re.S).group(1)
            if f in T: body = T[f](body)
            for k, v in NOTION.items(): body = body.replace(k, v)
            cls = {'desk': ' pg-desk', 'mob': ' pg-mob'}.get(mode, '')
            figs_html += f'<div class="pg-fig{cls}" id="{fid}">{body}</div>'
        tag = f'<span class="pg-tagst">STEP {cur}</span>' if (cur and not opts.get('notag') and not first) else ''
        first = False
        back = cfg.get('back')
        bk = '' if (opts.get('noback') or not back) else f'<a class="pg-back" href="{back[0]}">{back[1]}</a>'
        h2 = f'<h2>{title}</h2>' if title else ''
        cp = f'<p class="pg-cap">{html.escape(cap)}</p>' if cap else ''
        sections.append(f'<section class="pg-sec" id="{sid}">{tag}{h2}{cp}{figs_html}{bk}</section>')
    th = cfg['theme']
    css = f':root{{--th:{th[0]};--th2:{th[1]};--th3:{th[2]}}}\n' + PGCSS + cfg.get('css', '')
    css += '.pg-mob{display:none}\n.pg-band .pg-no{font-size:20px}\n.pg-nav{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px}.pg-nav a{color:#fff;text-decoration:none;font-size:13px;font-weight:700;border:1px solid rgba(255,255,255,.6);border-radius:999px;padding:1px 10px}.pg-nav a.on{background:#fff;color:var(--th)}\n'
    css += ''.join(desk)
    m = PGM.replace('/*MOB*/', ''.join(mob) + '\n.pg-desk{display:none!important}.pg-mob{display:block!important}\n.pg-fig .sub{font-size:16px!important;margin-bottom:10px!important}\n' + cfg.get('mcss', ''))
    nav = ''.join(f'<a href="{h}"{" class=on" if h == cfg["file"] else ""}>{l}</a>' for h, l in [('index.html', '目次'), ('odan.html', '横断パッケージ'), ('k-shiki.html', '蓄積型（K式）')])
    page = f'''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{cfg['title']}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&display=swap" rel="stylesheet">
<style>
{ROOT}
{css}
{m}
</style></head><body>
<header class="pg-top"><div class="pg-in"><nav class="pg-nav">{nav}</nav>{cfg['header']}</div></header>
<nav class="pg-toc"><div class="pg-wrap">{''.join(toc)}</div></nav>
{''.join(sections)}
<p class="pg-foot">{cfg.get('foot', '© BRDC Frontiers プロファイルセンター')}</p>
</body></html>'''
    page = soften(page)
    open('../site/' + cfg['file'], 'w').write(page)
    return len(page)


def sec(sid, title, cap, figs, **opts):
    return ('sec', sid, title, cap, figs, opts)


CYC = '''<div class="mcyc"><div style="--c:#e0561b">📊 <b>農場プロファイル</b><small>農場全体を広く見る</small></div><i>▼</i><div style="--c:#c28a00;background:#fdf5dc">🔍 <b>Check！</b><small>SeFレポートで問題発見</small></div><i>▼</i><div style="--c:#2f6688;background:#e6eef3">🔬 <b>Add-on解析</b><small>原因を深く調べる</small></div><i>▼</i><div style="--c:#2f7d3a;background:#eaf5eb">🛠️ <b>Act</b><small>対策を決めて実行</small></div><i>▼</i><div style="--c:#6b3fa0">🔁 <b>Re-profile</b><small>対策した段階を測り直す</small></div><i class="up">↺ 農場プロファイルにもどって、くり返す</i></div>'''


def tf_g6(b):
    return b.replace('<svg viewBox="0 0 944 560"', CYC + '<svg class="dcyc" viewBox="0 0 944 560"')


def tf_g4_form(b):
    return b.replace('<div class="bot">このあとは、選んだルートのSOPページへ ▶</div>', f'<div class="bot"><a class="pg-btn" href="{FORM}" target="_blank" rel="noopener">📝 申請フォームを開く</a></div>')


def tf_g4_index(b):
    return b.replace('<div class="bot">このあとは、選んだルートのSOPページへ ▶</div>', f'<div class="bot"><a class="pg-btn" href="{FORM}" target="_blank" rel="noopener">📝 申請フォームを開く</a><div class="pg-after">このあとは、選んだルートのSOPへ：<a href="odan.html">横断パッケージ ›</a>　<a href="k-shiki.html">蓄積型（K式） ›</a></div></div>')


def tf_g2(b):
    import re as _re
    def wrap(m):
        div=m.group(0)
        if '横断パッケージ' in div: href='odan.html'
        elif 'K式' in div: href='k-shiki.html'
        else: return div
        div=div.replace('<small>',' ›<small>',1)
        return f'<a class="resl" href="{href}" xmlns="http://www.w3.org/1999/xhtml">'+div+'</a>'
    return _re.sub(r'<div class="res"[^>]*>.*?</div>', wrap, b)


def flow_links(steps, figid, side=None):
    def tf(body):
        def rep(m):
            n = int(m.group(2))
            lab = steps[n - 1][3]
            return f'<a class="stl" href="#step{n}">' + m.group(0).replace('</small></div></div>', f'</small><em class="go">{lab} ›</em></div></div>') + '</a>'
        body = re.sub(r'<div class="st( \w+)?"><div class="n">(\d)</div><div>.*?</small></div></div>', rep, body)
        if side: body = body.replace(side[0], side[1])
        return body
    return tf


FLOWCSS = lambda fid: f'''
#{fid} a.stl{{display:block;text-decoration:none;color:inherit;border-radius:14px;transition:transform .12s, box-shadow .12s}}
#{fid} a.stl:hover .st,#{fid} a.stl:focus .st{{box-shadow:0 0 0 3px #ffe08a;transform:translateY(-1px)}}
#{fid} .go{{display:table;margin-top:5px;font-style:normal;font-size:14px;font-weight:900;color:#fff;background:var(--th);border-radius:999px;padding:1px 12px}}
#{fid} .st.end .go{{background:#c2362b}}
#{fid} .st.res .go{{background:#1c2622}}
#{fid} .side a{{color:#5c4900;font-weight:900;text-decoration:underline}}
'''
COMMON_G = '''
.pg-top p.pg-orig{font-size:13px;opacity:.85;margin-top:6px}

.pg-fig > .w{width:100%!important;max-width:1000px}

.pg-btn{display:block!important;width:max-content;max-width:100%;margin:6px auto 0;background:#d42a1e!important;color:#fff!important;text-decoration:none;font-weight:900!important;font-size:clamp(20px,4.6vw,28px)!important;border-radius:999px;padding:16px 44px!important;box-shadow:0 5px 0 #8f1a10,0 8px 18px rgba(212,42,30,.35);animation:pgpulse 2.4s ease-in-out infinite}
.pg-btn:hover{transform:translateY(-2px)}
.pg-btn::after{content:" ›"}
@keyframes pgpulse{0%,100%{box-shadow:0 5px 0 #8f1a10,0 8px 18px rgba(212,42,30,.35)}50%{box-shadow:0 5px 0 #8f1a10,0 8px 28px rgba(212,42,30,.6)}}
.pg-lead a.pg-cta{background:#d42a1e!important;color:#fff!important;font-size:18px!important;padding:10px 20px!important;box-shadow:0 3px 0 #8f1a10;border:2px solid #fff}
@media (prefers-reduced-motion:reduce){.pg-btn{animation:none}}
@media (max-width:960px){.pg-btn{white-space:nowrap;font-size:21px!important;padding:14px 26px!important}}

#xg4 .n{display:none!important}
#xg4 .bot{background:none!important}
.pg-after{margin-top:8px;font-size:15px;font-weight:700;color:#5d6a64}.pg-after a{color:#c8361c;font-weight:900}
'''

# ---------------- 横断 ----------------
OSTEPS = [(1, '申請フォームで申請', '申請', '申請のしかたへ'),
          (2, '配置図を修正して、実施日をメールで連絡', '配置図・実施日', '配置図と連絡内容へ'),
          (3, '採材シートを作り、キットが届く', '準備', '採材牛の条件とキットへ'),
          (4, '実施日：採材・撮影', '実施日', '採材・撮影の方法へ'),
          (5, '冷凍便で発送して、アップロード', '発送', '発送とアップロードへ'),
          (6, '結果レポートが返ってくる', '結果', '結果の見かたへ')]
odan_items = [sec('s-flow', '横断パッケージの流れ', '各ステップを押すと、その説明へ移動します', ['o_flow'], noback=True, toc=('流れ', '▶')),
              sec('s-sheet', 'いつでもOK：農場聞き取りシート', '', ['o_sheet'], toc=('聞き取り', '✎'))]
for n, full, short, _ in OSTEPS:
    odan_items.append(('step', n, full, short))
    if n == 1: odan_items.append(sec('s-apply', '申請のしかた', 'Googleアカウントを用意 → 農場のGoogle Map情報 → 申請フォームで「横断パッケージ」を選ぶ → 共有フォルダのアドレスがメールで届く', ['g4', 'o_gmap']))
    if n == 2:
        odan_items.append(sec('s-haichi', '配置図の修正（記入例）', '共有フォルダの「農場名　農場配置ファイル」で番号を確認し、表に牛舎の詳細を書きます', ['haichi']))
        odan_items.append(sec('s-mail', '実施日をメールで連絡', '農場と実施日を相談してから、センターへ', ['o_mail']))
    if n == 3:
        odan_items.append(sec('s-cows', '採材シート：採材する牛の条件', '共有フォルダの「農場名　採材シート」に、採材する子牛を書き出します', ['o_cows']))
        odan_items.append(sec('s-kit', 'キットの中身', '届いたら、物品チェックリストで確認', ['o_kit']))
    if n == 4: odan_items.append(sec('s-day', '実施日の採材と撮影', '複数日に分けてもOK。先に動画を見てから。牛は採材サポートカード、農場は撮影サポートカードに従って', ['o_day']))
    if n == 5: odan_items.append(sec('s-after', '発送とアップロード', 'サンプルは冷凍便。データは共有フォルダかフォームから', ['o_after']))
    if n == 6:
        odan_items.append(sec('s-g5', 'プロファイル結果', '１か月以内に返送。獣医師向けの「SeF生データ」と、農家さん向けの「SeFレポート」', ['g5', 'o_report']))
        odan_items.append(sec('s-g6', 'Add-on解析で「Act」まで', '問題が見えたところだけを深く調べ、対策につなげて、効果まで確かめる', ['g6']))
        odan_items.append(sec('s-g7', 'Add-on解析　お悩み別メニュー', 'SeFレポートの提案を見て、センターへメールでご相談ください', ['g7']))
odan_items.append(('band', 'detail', '詳細SOP（困ったときに）', '詳細SOP', '📖'))
odan_items.append(sec('s-detail', '', '', ['o_detail'], notag=True))


def tf_haichi_odan(b):
    return b.replace('▼ この配置図をもとに、次の「Zoneとは」「Zoneの登録」でZoneを決めます', '▼ 書けたら、農場と実施日を相談して、センターへメール（下）')


ODAN = dict(file='odan.html', title='横断パッケージ 実施SOP｜農場プロファイル', theme=('#c8361c', '#fdeee9', '#f1b9a6'),
            header='<span class="pg-tag">農場プロファイル</span><h1>横断パッケージ 実施SOP</h1><p>採材する日を決めて、農場全体（15頭）をまとめて評価します。1日で終わらなければ、複数日に分けてもOK。</p><div class="pg-lead"><a class="pg-cta" href="'+FORM+'" target="_blank" rel="noopener">📝 申請フォームを開く</a><a href="#s-flow">はじめから見る ▶</a><a href="https://youtu.be/no0Gnvm21ps?si=VB3FtnRJIXhM50e8" target="_blank" rel="noopener">▶ 実践ガイド動画</a><a href="#step6">📊 結果の見かた</a></div>',
            items=odan_items, back=('#s-flow', '▲ 流れにもどる'),
            tf={'o_flow': flow_links(OSTEPS, 'xo_flow', ('<div class="side" style="margin:0 0 10px">いつでもOK：農場聞き取りシート</div>', '<div class="side" style="margin:0 0 10px">いつでもOK：<a href="#s-sheet">農場聞き取りシート ›</a></div>')),
                'g4': tf_g4_form, 'g6': tf_g6, 'haichi': tf_haichi_odan},
            css=FLOWCSS('xo_flow') + COMMON_G + '#xg6 .lead{display:none}#xg6 .mcyc{display:none}\n#xg4 + #xo_gmap{margin-top:8px}\n',
            foot='Notionの横断パッケージ実施SOPと同じ内容です。　© BRDC Frontiers プロファイルセンター')

# ---------------- 目次 ----------------
INDEX = dict(file='index.html', title='農場プロファイル実施SOP｜BRDC Frontiers', theme=('#e0561b', '#fff3ea', '#f3c7a8'),
             header='<span class="pg-tag">BRDC Frontiers</span><h1>📊 農場プロファイル実施SOP</h1><p>2つのルートから選べます。評価する「ものさし」は同じです。</p><div class="pg-lead"><a class="pg-cta" href="' + FORM + '" target="_blank" rel="noopener">📝 申請フォームを開く</a><a href="odan.html">🟥 横断パッケージ</a><a href="k-shiki.html">🟩 蓄積型（K式）</a></div>',
             items=[sec('s-apply', '申請はこちらから', '', ['o_apply'], noback=True, toc=('申請', '📝')),
                    sec('s-media', '説明動画・説明漫画', 'はじめての方は、まずこちらで全体をつかんでください', ['o_media'], toc=('動画・漫画', '🎬')),
                    sec('s-route', '実施方法をえらぶ', '決めた日にまとめて実施する横断パッケージと、診療・農場フローの中で少しずつためていく蓄積型（K式）、どちらも集めるデータは同じです', ['g1', ('g2', 'desk'), ('o_choose', 'mob')], toc=('えらぶ', '🔀')),
                    sec('s-sop', '各ルートの実施SOP', 'カードを押すと、それぞれの実施SOPページへ移動します', ['o_routes'], toc=('実施SOP', '📋')),
                    sec('s-howto', '申請のしかた（共通）', 'Googleアカウント → Google Map情報 → 申請フォーム（実施方法を選ぶ）→ センターからメール', ['g4', 'o_gmap'], toc=('申請のしかた', '❓')),
                    sec('s-result', 'プロファイル結果（１か月以内に返送）', '獣医師向けの「SeF生データ」（Excel）と、農家さん向けの「SeFレポート」', ['g5', 'o_report'], toc=('結果', '📊')),
                    sec('s-addon', '追加解析（Add-on）', 'SeFレポートで問題が見えたところだけを深く調べ、対策（Act）とその効果の確認まで支援します。申込みはメールでセンターへ', ['g6', 'g7'], toc=('Add-on', '🔬')),
                    sec('s-open', '', '', ['o_open'], toc=('オープン化', 'ⓘ'))],
             back=('#s-apply', '▲ 上にもどる'),
             tf={'g4': tf_g4_index, 'g6': tf_g6, 'g2': tf_g2},
             css=COMMON_G + '#xg6 .lead{display:none}#xg6 .mcyc{display:none}\n#xg6 + #xg7{margin-top:14px}\n#xg2 a.resl{display:block;text-decoration:none;cursor:pointer}#xg2 a.resl .res{transition:transform .12s,box-shadow .12s;box-shadow:0 3px 0 rgba(0,0,0,.25)}#xg2 a.resl:hover .res{transform:translateY(-2px);box-shadow:0 0 0 3px #ffe08a,0 3px 0 rgba(0,0,0,.25)}\n#xg1 .h1,#xg1 .lead{display:none}#xg1 .sh{display:block!important}#xg1 .sec{border:2px solid #f3c7a8!important}\n',
             foot='© BRDC Frontiers プロファイルセンター')

# ---------------- K式 ----------------
KSTEPS=[(1,'申請フォームで申請','申請','申請のしかたへ'),
(2,'配置図を修正して、Zoneを登録','Zone登録','配置図とZoneの説明へ'),
(3,'キット（コンテナ）が届く','キット','キットの中身へ'),
(4,'期限までに、採材・撮影','採材・撮影','採材と撮影へ'),
(5,'終わりにする（先生が判断）','終わりにする','目安の頭数へ'),
(6,'アップロードと発送','発送','アップロードと発送へ'),
(7,'結果レポートが返ってくる','結果','結果の見かたへ')]
KF={1:[('g4','申請のしかた','Googleアカウントを用意 → 農場のGoogle Map情報 → 申請フォームで「K式」を選ぶ → 共有フォルダのアドレスがメールで届く',['g4','o_gmap'])],
2:[('haichi_k','配置図の修正（記入例）','センターが番号をふった配置図を確認し、表に牛舎の詳細を書きます',None),('fig3a','Zoneとは','牛の段階・収容方法・空間と換気・飼料と哺乳の4つが同じ場所が1つのZone',None),('fig3b','Zoneの登録','分娩60日前からの母牛と、135日齢までの子牛がいる場所を登録',None)],
3:[('fig4','キットの中身','NPS採取用チューブ25本（色付きキャップ：緑16・橙6・赤3）と白カード5枚',None)],
4:[('fig5','牛1頭ずつ：個体の撮り方','スマホは縦・1頭1本：チューブ → 胸囲（声）→ Zone名（声）→ 耳標 → 顔 → 横 → 後ろ',None),('fig10','NPSの採り方','下・斜め内側へ入れ、咽頭壁で10回まわす。チューブは立てたまま冷凍庫へ',None),('fig8','Zoneの撮影','時間のあるときに。スマホは横・1Zone 1本・止めずに：カード → Zone全体（消毒槽、水槽・水桶に寄る）→ ＋α',None),('fig9','Zoneカードの例','牛房サイズを書いて、撮るところを番号順に',None),('fig7','農場の聞き取り','時間のあるときに。紙に手書きして写真、またはPDFに直接入力。どちらでもOK',['fig7','o_sheetlink'])],
5:[('fig11','なぜ、この頭数なの？','目安の数が集まったら、または期限が来たら終わり。NPS（緑・橙）は目標15頭 → 目安8頭以上 → 最低5頭',None)],
6:[('fig6','共有フォルダとアップロード','アップロードは後日まとめてOK。発送したらセンターにメール。個体の動画は牛の日齢のフォルダへ',None)],
7:[('g5','プロファイル結果','１か月以内に返送。獣医師向けの「SeF生データ」と、農家さん向けの「SeFレポート」',['g5','o_report']),('g6','Add-on解析で「Act」まで','問題が見えたところだけを深く調べ、対策につなげて、効果まで確かめる',None),('g7','Add-on解析　お悩み別メニュー','SeFレポートの提案を見て、センターへメールでご相談ください',None)]}
k_items=[sec('s-fig2k','蓄積型（K式）の流れ','各ステップを押すと、その説明へ移動します',['fig2k'],noback=True,toc=('流れ','▶'))]
for n,full,short,_ in KSTEPS:
    k_items.append(('step',n,full,short))
    for f,t,c,figs in KF[n]:
        k_items.append(sec('s-'+f,t,c,figs or [f]))
def tf_fig5(body):
    body=body.replace('<div class="bb">\n <div class="pre">','<div class="bb">\n <div class="pgh">🎬 動画を撮る前に</div>\n <div class="pre"><span class="lab">NPSを採る牛</span>',1)
    body=body.replace(' <div class="pre"><div class="pc" style="border-color:#8a6d00',' <div class="pre p2"><span class="lab">0〜30日齢・胸囲だけの牛</span><div class="pc" style="border-color:#8a6d00',1)
    body=body.replace(' <div class="chain">',' <div class="pgh">📹 動画の中で撮る順番</div>\n <div class="chain">',1)
    return body
KSHIKI=dict(file='k-shiki.html',title='蓄積型（K式） 実施SOP｜農場プロファイル',theme=('#3f6b45','#e8f0e7','#cfe0cf'),
 header='<span class="pg-tag">農場プロファイル</span><h1>診療・農場フロー蓄積型パッケージ（K式）実施SOP</h1><p>日々の診療のついでに、期限までに少しずつ。1日でまとめてもOK。</p><p class="pg-orig">※「K式」は、臨床獣医師のK先生の方式にヒントを得た呼び名です。このサイトでは「蓄積型（K式）」と略します。</p><div class="pg-lead"><a class="pg-cta" href="'+FORM+'" target="_blank" rel="noopener">📝 申請フォームを開く</a><a href="#s-fig2k">はじめから見る ▶</a><a href="#step7">📊 結果の見かた</a><a href="K式_実施ガイド_A4印刷用.pdf">🖨 印刷用PDF（A4）</a></div>',
 items=k_items,back=('#s-fig2k','▲ 流れにもどる'),
 tf={'fig2k':flow_links(KSTEPS,'xfig2k',('<div class="side">時間のあるときに：Zoneの撮影・聞き取りシート</div>','<div class="side">時間のあるときに：<a href="#s-fig8">Zoneの撮影 ›</a>・<a href="#s-fig7">聞き取りシート ›</a></div>')),'g4':tf_g4_form,'g6':tf_g6,'fig5':tf_fig5},
 css=FLOWCSS('xfig2k')+COMMON_G+'#xg6 .lead{display:none}#xg6 .mcyc{display:none}\n',
 foot='くわしい手順（詳細SOP）は、蓄積型（K式）実施SOPのNotionページにあります。　© BRDC Frontiers プロファイルセンター')

if __name__ == '__main__':
    for c in (INDEX, ODAN, KSHIKI):
        print(c['file'], render(c))
