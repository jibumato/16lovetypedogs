#!/usr/bin/env python3
# JA OGPカード(ogp/ja/*.png)生成。ポップステッカー調（シェアカード案Aと世界観統一）。
# 依存: M PLUS Rounded 1c (/tmp/MPLUSRounded1c-{Regular,ExtraBold}.ttf) と /tmp/OGP_DATA.json
#   データ: index.html の LOC/I18N/RARITY/DOC_LINE と各タイプのベスト相性(best)を JSON ダンプしたもの
# 使い方: python3 generate_ja_ogp.py [CODE ...]   (引数なしは ogp/ja/ 全16生成)
import json, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT=os.path.dirname(os.path.abspath(__file__))
D=json.load(open("/tmp/OGP_DATA.json",encoding="utf-8"))
LOC=D["LOC"];I18N=D["I18N"];RARITY=D["RARITY"];DOC=D.get("DOC_LINE",{});BEST=D.get("best",{});ORDER=D["ORDER"]
REG="/tmp/MPLUSRounded1c-Regular.ttf";BOLD="/tmp/MPLUSRounded1c-ExtraBold.ttf"
PINK=(242,145,182);PURPLE=(185,138,232);WHITE=(255,255,255)
INK=(87,79,99);PINK_DEEP=(210,98,143);BOX=(255,253,248);GOLD=(184,138,58)
def fb(s):return ImageFont.truetype(BOLD,s)
def fr(s):return ImageFont.truetype(REG,s)
def wrap(dr,t,f,mw):
    o=[];ln=""
    for ch in list(t):
        if dr.textlength(ln+ch,font=f)>mw and ln:o.append(ln);ln=ch
        else:ln+=ch
    if ln:o.append(ln)
    return o
def fit(dr,t,mk,mw,mn=24):
    s=mk
    while s>mn and dr.textlength(t,font=fb(s))>mw:s-=2
    return fb(s)
def circle_mask(sz):
    m=Image.new("L",(sz,sz),0);ImageDraw.Draw(m).ellipse([0,0,sz-1,sz-1],fill=255);return m
def shadow_text(base,xy,text,font,fill=WHITE,anchor="lm",mw=None):
    """白文字＋淡い影（パステル背景でも読める）"""
    lay=Image.new("RGBA",base.size,(0,0,0,0));ld=ImageDraw.Draw(lay)
    ld.text((xy[0],xy[1]+3),text,font=font,fill=(120,55,95,150),anchor=anchor)
    lay=lay.filter(ImageFilter.GaussianBlur(4));base.alpha_composite(lay)
    ImageDraw.Draw(base).text(xy,text,font=font,fill=fill+(255,),anchor=anchor)

def make(code,lang="ja"):
    d=LOC[lang][code];W,H=1200,630
    img=Image.new("RGBA",(W,H),PINK+(255,))
    dr=ImageDraw.Draw(img)
    # 対角パープル
    dr.polygon([(W,0),(W,H),(0,H)],fill=PURPLE+(255,))
    # 散りドット
    for k in range(20):
        dr.ellipse([(k*197)%W,(k*271)%H,(k*197)%W+9,(k*271)%H+9],fill=(255,255,255,38))
    # 左：円形ステッカー＋犬
    ccx,ccy,r=300,290,214
    circ=Image.new("RGBA",(2*r,2*r),(0,0,0,0));cd=ImageDraw.Draw(circ)
    sh=Image.new("RGBA",(W,H),(0,0,0,0));ImageDraw.Draw(sh).ellipse([ccx-r,ccy-r+10,ccx+r,ccy+r+10],fill=(120,70,110,70))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
    dr.ellipse([ccx-r,ccy-r,ccx+r,ccy+r],fill=WHITE+(255,))
    dp=os.path.join(ROOT,f"{code.lower()}.png");DS=2*(r-8)
    if os.path.exists(dp):
        dog=Image.open(dp).convert("RGBA");sc=max(DS/dog.width,DS/dog.height)
        dog=dog.resize((int(dog.width*sc),int(dog.height*sc)))
        l=(dog.width-DS)//2;t=(dog.height-DS)//2;dog=dog.crop((l,t,l+DS,t+DS))
        base=Image.new("RGBA",(DS,DS),WHITE+(255,));base.alpha_composite(dog)
        img.paste(base,(ccx-DS//2,ccy-DS//2),circle_mask(DS))
    # 犬種（円の下・白）
    bf=fit(dr,d["breed"],52,500,30)
    shadow_text(img,(ccx,ccy+r+50),d["breed"],bf,anchor="mm")
    shadow_text(img,(ccx,ccy+r+96),f"{code} ・ {d.get('role','')}",fr(26),anchor="mm")
    # 右：コード＋肩書き
    RX=600
    shadow_text(img,(RX,86),code,fb(76),anchor="lm")
    ny=150
    for ln in wrap(dr,d["name"],fb(38),W-RX-40)[:2]:
        shadow_text(img,(RX,ny),ln,fb(38),anchor="lm");ny+=52
    # わんこ博士のひとこと（白箱）
    doc=(DOC.get(code) if lang=="ja" else None) or ("「"+(d.get("hook") or d.get("tag",""))+"」")
    bx1,by1,bx2=RX,ny+16,W-46
    lines=wrap(dr,doc,fr(25),bx2-bx1-40)[:3]
    by2=by1+54+len(lines)*37+16
    dr.rounded_rectangle([bx1,by1,bx2,by2],24,fill=BOX+(255,))
    dr.text(((bx1+bx2)//2,by1+30),"― わんこ博士のひとこと ―",font=fb(24),fill=PINK_DEEP,anchor="mm")
    ty=by1+66
    for ln in lines:dr.text(((bx1+bx2)//2,ty),ln,font=fr(25),fill=INK,anchor="mm");ty+=37
    # ベスト相性ティーザー（ピンクピル）
    bc=BEST.get(code);best_breed=LOC[lang].get(bc,{}).get("breed","") if bc else ""
    if best_breed:
        pt=f"ベスト相性は、、、{best_breed} etc"
        pf=fit(dr,pt,26,W-RX-60,18);pw=int(dr.textlength(pt,font=pf))+44
        py1=by2+18;ph=54
        dr.rounded_rectangle([RX,py1,RX+pw,py1+ph],ph//2,fill=(232,77,128,255))
        dr.text((RX+pw//2,py1+ph//2),pt,font=pf,fill=WHITE,anchor="mm")
    # 巻き込みCTA（下部・白）
    shadow_text(img,(RX,H-58),"あなたは何わんこ？ ▶ 16lovetypedogs.com",fb(28),anchor="lm")
    return img.convert("RGB")

codes=sys.argv[1:] or ORDER
outdir=os.path.join(ROOT,"ogp","ja");os.makedirs(outdir,exist_ok=True)
for c in codes: make(c).save(os.path.join(outdir,c.lower()+".png"));print("saved",c)
