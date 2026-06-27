#!/usr/bin/env python3
# JA OGPカード(ogp/ja/*.png)生成。長い犬種名は左カラム幅に縮小フィットさせ右カードへの被りを防ぐ。
# 依存: M PLUS Rounded 1c (/tmp/MPLUSRounded1c-{Regular,ExtraBold}.ttf) と /tmp/LOC.json /tmp/I18N.json
#   フォント: https://github.com/google/fonts/raw/main/ofl/mplusrounded1c/MPLUSRounded1c-{Regular,ExtraBold}.ttf
#   データ: index.html の LOC / I18N を JSON ダンプしたもの
# 使い方: python3 generate_ja_ogp.py [CODE ...]   (引数なしは ogp/ja/ 全16生成)
import json, os, sys
from PIL import Image, ImageDraw, ImageFont
ROOT=os.path.dirname(os.path.abspath(__file__))
LOC=json.load(open("/tmp/LOC.json",encoding="utf-8"));I18N=json.load(open("/tmp/I18N.json",encoding="utf-8"))
REG="/tmp/MPLUSRounded1c-Regular.ttf";BOLD="/tmp/MPLUSRounded1c-ExtraBold.ttf"
CREAM=(252,244,239);BLOB=(247,224,233);PINK=(210,98,143);PINK_BD=(242,184,204)
PILL_BG=(247,217,228);INK=(87,79,99);INK_SOFT=(147,138,163);WHITE=(255,255,255)
def fb(s):return ImageFont.truetype(BOLD,s)
def fr(s):return ImageFont.truetype(REG,s)
def wrap(dr,t,f,mw):
    o=[];ln=""
    for ch in list(t):
        if dr.textlength(ln+ch,font=f)>mw and ln:o.append(ln);ln=ch
        else:ln+=ch
    if ln:o.append(ln)
    return o
def rmask(sz,r):
    m=Image.new("L",sz,0);ImageDraw.Draw(m).rounded_rectangle([0,0,sz[0]-1,sz[1]-1],r,fill=255);return m
def make(code,lang="ja"):
    d=LOC[lang][code];W,H=1200,630
    img=Image.new("RGB",(W,H),CREAM)
    blob=Image.new("RGBA",(W,H),(0,0,0,0));bd=ImageDraw.Draw(blob)
    bd.ellipse([-140,-180,220,180],fill=BLOB+(120,));bd.ellipse([W-260,H-220,W+120,H+160],fill=BLOB+(110,))
    img=Image.alpha_composite(img.convert("RGBA"),blob).convert("RGB");dr=ImageDraw.Draw(img)
    LX=60;LW=600
    ef=fb(26);et="MBTI  ×  恋愛  ×  犬種";ew=dr.textlength(et,font=ef)
    dr.rounded_rectangle([LX,44,LX+ew+48,96],26,fill=PILL_BG);dr.text((LX+24,70),et,font=ef,fill=PINK,anchor="lm")
    y=124;dr.text((LX,y),"私の恋愛わんこは",font=fr(34),fill=INK_SOFT,anchor="lm");y+=54
    bs=92
    while bs>40 and dr.textlength(d["breed"],font=fb(bs))>LW:bs-=4
    dr.text((LX,y),d["breed"],font=fb(bs),fill=PINK,anchor="lm");y+=bs//2+34
    dr.text((LX,y),f"({code})",font=fb(34),fill=INK_SOFT,anchor="lm");y+=54
    for ln in wrap(dr,d["name"],fb(38),LW)[:2]:dr.text((LX,y),ln,font=fb(38),fill=INK,anchor="lm");y+=48
    y+=6
    for ln in wrap(dr,d["tag"],fr(28),LW)[:3]:dr.text((LX,y),ln,font=fr(28),fill=INK_SOFT,anchor="lm");y+=38
    dr.line([LX,H-92,LX+LW,H-92],fill=PINK_BD,width=2)
    dr.text((LX,H-58),f"16lovetypedogs.com    #{I18N[lang]['hashtag']}",font=fr(26),fill=INK_SOFT,anchor="lm")
    CW,CH=410,478;CX,CY=W-CW-70,(H-CH)//2
    img.paste(Image.new("RGB",(CW,CH),WHITE),(CX,CY),rmask((CW,CH),34))
    dr.rounded_rectangle([CX,CY,CX+CW,CY+CH],34,outline=PINK_BD,width=4)
    dp=os.path.join(ROOT,f"{code.lower()}.png");DS=288
    if os.path.exists(dp):
        dog=Image.open(dp).convert("RGBA");s=max(DS/dog.width,DS/dog.height)
        dog=dog.resize((int(dog.width*s),int(dog.height*s)))
        l=(dog.width-DS)//2;t=(dog.height-DS)//2;dog=dog.crop((l,t,l+DS,t+DS))
        bg=Image.new("RGBA",(DS,DS),WHITE+(255,));bg.alpha_composite(dog)
        img.paste(bg.convert("RGB"),(CX+(CW-DS)//2,CY+30),rmask((DS,DS),26))
    tcx=CX+CW//2
    dr.text((tcx,CY+348),code,font=fb(30),fill=INK_SOFT,anchor="mm")
    bsz=40
    while bsz>22 and dr.textlength(d["breed"],font=fb(bsz))>CW-56:bsz-=2
    dr.text((tcx,CY+388),d["breed"],font=fb(bsz),fill=PINK,anchor="mm")
    dr.text((tcx,CY+422),d.get("role",""),font=fr(24),fill=INK_SOFT,anchor="mm")
    dr.line([CX+40,CY+444,CX+CW-40,CY+444],fill=PINK_BD,width=2)
    dr.text((tcx,CY+462),"16わんこ恋愛診断  結果",font=fr(22),fill=INK_SOFT,anchor="mm")
    return img

ORDER=["INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP","ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"]
import sys as _sys
codes=_sys.argv[1:] or ORDER
outdir=os.path.join(ROOT,"ogp","ja");os.makedirs(outdir,exist_ok=True)
for c in codes: make(c).save(os.path.join(outdir,c.lower()+".png"));print("saved",c)
