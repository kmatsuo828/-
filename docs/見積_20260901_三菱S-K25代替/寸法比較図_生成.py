# -*- coding: utf-8 -*-
SP='/tmp/claude-0/-home-user--/bdd2ed83-699d-5548-985c-f70774d98b1a/scratchpad'
S=2.55 # px per mm

UNITS=[
 dict(name='S-K25', tag='既設・生産終了', W=80,H=89,D=102, pw=71,ph=65, col='#8a8a8a', fill='#f0f0f0'),
 dict(name='S-T25', tag='代替候補 ①',     W=63,H=81,D=81,  pw=54,ph=60, col='#1a4f8a', fill='#e8f0fa'),
 dict(name='S-T35', tag='代替候補 ②',     W=75,H=89,D=91,  pw=65,ph=70, col='#0b7a4b', fill='#e6f5ee'),
]
CW=340          # column width
BASE=330        # baseline y for body bottom
X0=66           # 左端をそろえる（比較しやすいように左揃え）

def dim_h(x1,x2,y,label,col='#333'):
    # horizontal dimension line with arrows
    return (f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{col}" stroke-width="1.6"/>'
            f'<line x1="{x1}" y1="{y-7}" x2="{x1}" y2="{y+7}" stroke="{col}" stroke-width="1.6"/>'
            f'<line x1="{x2}" y1="{y-7}" x2="{x2}" y2="{y+7}" stroke="{col}" stroke-width="1.6"/>'
            f'<text x="{(x1+x2)/2}" y="{y+26}" text-anchor="middle" font-size="21" fill="{col}">{label}</text>')

def dim_v(y1,y2,x,label,col='#333'):
    return (f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{col}" stroke-width="1.6"/>'
            f'<line x1="{x-7}" y1="{y1}" x2="{x+7}" y2="{y1}" stroke="{col}" stroke-width="1.6"/>'
            f'<line x1="{x-7}" y1="{y2}" x2="{x+7}" y2="{y2}" stroke="{col}" stroke-width="1.6"/>'
            f'<text x="{x-14}" y="{(y1+y2)/2}" text-anchor="middle" font-size="21" fill="{col}"'
            f' transform="rotate(-90 {x-14} {(y1+y2)/2})">{label}</text>')

def front(u):
    w,h=u['W']*S,u['H']*S
    x0=X0; y0=BASE-h
    cx=x0+w/2; cy=y0+h/2
    hx=u['pw']*S/2; hy=u['ph']*S/2
    s=[f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="4" fill="{u["fill"]}" stroke="{u["col"]}" stroke-width="3"/>']
    s.append(f'<rect x="{x0+6}" y="{y0+6}" width="{w-12}" height="15" fill="#fff" stroke="{u["col"]}" stroke-width="1.2" opacity=".75"/>')
    s.append(f'<rect x="{x0+6}" y="{y0+h-21}" width="{w-12}" height="15" fill="#fff" stroke="{u["col"]}" stroke-width="1.2" opacity=".75"/>')
    s.append(f'<rect x="{cx-hx}" y="{cy-hy}" width="{hx*2}" height="{hy*2}" fill="none" stroke="#c0392b" stroke-width="1.5" stroke-dasharray="7 5"/>')
    for dx in(-hx,hx):
        for dy in(-hy,hy):
            s.append(f'<circle cx="{cx+dx}" cy="{cy+dy}" r="6" fill="#fff" stroke="#c0392b" stroke-width="2.4"/>')
            s.append(f'<line x1="{cx+dx-9.5}" y1="{cy+dy}" x2="{cx+dx+9.5}" y2="{cy+dy}" stroke="#c0392b" stroke-width="1.2"/>')
            s.append(f'<line x1="{cx+dx}" y1="{cy+dy-9.5}" x2="{cx+dx}" y2="{cy+dy+9.5}" stroke="#c0392b" stroke-width="1.2"/>')
    # 引出線（取付穴 → 下のピッチ寸法線 / 右の縦ピッチ寸法線）
    for dx in(-hx,hx):
        s.append(f'<line x1="{cx+dx}" y1="{cy+hy}" x2="{cx+dx}" y2="{BASE+80}" stroke="#c0392b" stroke-width="0.9" stroke-dasharray="4 4" opacity=".7"/>')
    for dy in(-hy,hy):
        s.append(f'<line x1="{cx+hx}" y1="{cy+dy}" x2="{x0+w+30}" y2="{cy+dy}" stroke="#c0392b" stroke-width="0.9" stroke-dasharray="4 4" opacity=".7"/>')
    s.append(dim_h(x0,x0+w,BASE+30,f'幅 {u["W"]}'))
    s.append(dim_h(cx-hx,cx+hx,BASE+80,f'取付ピッチ 横 {u["pw"]}','#c0392b'))
    s.append(dim_v(y0,BASE,x0-30,f'高さ {u["H"]}'))
    s.append(dim_v(cy-hy,cy+hy,x0+w+30,f'縦 {u["ph"]}','#c0392b'))
    return ''.join(s)

def side(u):
    d,h=u['D']*S,u['H']*S
    x0=X0; y0=BASE-h
    s=[f'<rect x="{x0}" y="{y0}" width="{d}" height="{h}" rx="4" fill="{u["fill"]}" stroke="{u["col"]}" stroke-width="3"/>']
    s.append(f'<line x1="{x0}" y1="{y0+18}" x2="{x0+d}" y2="{y0+18}" stroke="{u["col"]}" stroke-width="1.2" opacity=".6"/>')
    s.append(f'<line x1="{x0}" y1="{y0+h-18}" x2="{x0+d}" y2="{y0+h-18}" stroke="{u["col"]}" stroke-width="1.2" opacity=".6"/>')
    s.append(dim_h(x0,x0+d,BASE+30,f'奥行 {u["D"]}'))
    s.append(dim_v(y0,BASE,x0-30,f'高さ {u["H"]}'))
    return ''.join(s)

def col(u,body,cap):
    return (f'<div class="col"><div class="cap"><b style="color:{u["col"]}">{u["name"]}</b>'
            f'<span>{u["tag"]}</span></div>'
            f'<svg width="{CW}" height="{BASE+118}" viewBox="0 0 {CW} {BASE+118}">{body}</svg>'
            f'<div class="sub">{cap}</div></div>')

fronts=''.join(col(u,front(u),f'外形 幅{u["W"]} × 高{u["H"]}') for u in UNITS)
sides =''.join(col(u,side(u), f'奥行 <b>{u["D"]}</b> × 高{u["H"]}') for u in UNITS)

html=f'''<!doctype html><html lang="ja"><head><meta charset="utf-8"><style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1080px;background:#fff;padding:44px 30px 40px;
 font-family:"Noto Sans CJK JP","Noto Sans JP","Hiragino Sans",sans-serif;color:#111}}
h1{{font-size:48px;color:#1a4f8a;border-bottom:6px solid #1a4f8a;padding-bottom:18px}}
.lead{{font-size:28px;margin:18px 0 6px;line-height:1.55}}
h2{{font-size:34px;background:#1a4f8a;color:#fff;padding:12px 22px;border-radius:8px;margin:34px 0 6px}}
h2 small{{font-size:24px;font-weight:400;margin-left:14px}}
.row{{display:flex;justify-content:space-between}}
.col{{width:{CW}px;text-align:center}}
.cap{{font-size:32px;margin-bottom:2px}}
.cap span{{display:block;font-size:22px;color:#666;font-weight:400;margin-top:2px}}
.sub{{font-size:24px;color:#333;margin-top:2px;line-height:1.5}}
.legend{{font-size:23px;color:#555;margin-top:10px;text-align:right}}
.note{{background:#fff4f2;border-left:10px solid #c0392b;padding:22px 26px;border-radius:6px;margin-top:34px}}
.note li{{font-size:28px;line-height:1.7;margin-left:32px}}
.foot{{margin-top:26px;font-size:23px;color:#666;line-height:1.6}}
table{{width:100%;border-collapse:collapse;margin-top:20px;font-size:26px}}
th,td{{border:2px solid #c9d3de;padding:12px 10px;text-align:center}}
th{{background:#1a4f8a;color:#fff}}
td.n{{font-weight:700}}
tr.old td{{background:#f4f4f4;color:#555}}
</style></head><body>
<h1>三菱電機 S-K25 / S-T25 / S-T35 寸法比較図</h1>
<div class="lead">同一縮尺で作図し、左端と底面をそろえています。赤い破線と⊕が<b>取付穴のピッチ</b>です。</div>

<h2>正面図<small>幅 × 高さ ／ 取付ピッチ（mm）</small></h2>
<div class="row">{fronts}</div>
<div class="legend">単位：mm　　⊕＝取付穴</div>

<h2>側面図<small>奥行 × 高さ（mm）</small></h2>
<div class="row">{sides}</div>
<div class="legend">単位：mm</div>

<h2>寸法一覧<small>単位 mm</small></h2>
<table>
<tr><th>品番</th><th>幅</th><th>高さ</th><th>奥行</th><th>取付ピッチ 横</th><th>取付ピッチ 縦</th></tr>
<tr class="old"><td>S-K25（既設）</td><td class="n">80</td><td class="n">89</td><td class="n">102</td><td class="n">71</td><td class="n">65</td></tr>
<tr><td>S-T25</td><td class="n">63</td><td class="n">81</td><td class="n">81</td><td class="n">54</td><td class="n">60</td></tr>
<tr><td>S-T35</td><td class="n">75</td><td class="n">89</td><td class="n">91</td><td class="n">65</td><td class="n">70</td></tr>
</table>

<div class="note"><ul>
<li><b>取付ピッチが3機種とも違うため、取付互換はありません。</b>変換アダプタの設定もありません。</li>
<li>S-T25／S-T35 とも S-K25 より小さくなります（特に奥行）。</li>
<li>既設のヒーター（サーマル）は流用できません。</li>
</ul></div>
<div class="foot">※ 寸法は因幡電機産業（株）様よりご提供いただいた数値に基づく作図です。<br>
※ 取付面の詳細・端子位置はメーカー外形図をご確認ください。</div>
</body></html>'''
open(SP+'/zumen_hikaku.html','w',encoding='utf-8').write(html)
print('written')
