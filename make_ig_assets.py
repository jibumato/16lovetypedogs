#!/usr/bin/env python3
"""Generate Instagram-ready (1080x1080) image assets for 16わんこ恋愛診断."""
import json, re, os
from PIL import Image, ImageDraw, ImageFont

ROOT=os.path.dirname(os.path.abspath(__file__))
OUT="/tmp/instagram_kit/assets/type_cards"
OUTA="/tmp/instagram_kit/assets"
src=open(os.path.join(ROOT,"index.html"),encoding="utf-8").read()
LOC=json.loads(re.search(r'\nconst LOC=(\{.*?\});\n',src,re.DOTALL).group(1))["ja"]
BASE=json.loads(re.search(r'\nconst BASE=(\{.*?\});\n',src,re.DOTALL).group(1))
ORDER=["INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP","ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"]

CREAM=(252,244,239); PINK=(210,98,143); INK=(87,79,99); INK_SOFT=(147,138,163); WHITE=(255,255,255)
PINK_BD=(242,184,204); PILL=(247,217,228)
GTINT={"NT":(244,238,251),"NF":(255,241,243),"SJ":(238,249,243),"SP":(255,246,233)}
GCOL={"NT":(194,164,239),"NF":(246,160,193),"SJ":(146,215,188),"SP":(244,192,111)}
JP="/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"
def f(sz): return ImageFont.truetype(JP, sz)

def rounded(size,r):
    m=Image.new("L",size,0); ImageDraw.Draw(m).rounded_rectangle([0,0,size[0]-1,size[1]-1],r,fill=255); return m

def blobs(img):
    W,H=img.size; ov=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    d.ellipse([-160,-200,260,200],fill=(247,224,233,120))
    d.ellipse([W-300,H-260,W+140,H+180],fill=(236,226,251,110))
    return Image.alpha_composite(img.convert("RGBA"),ov).convert("RGB")

def center_text(d,cx,y,text,font,fill,maxw=None):
    if maxw:
        # shrink to fit
        while d.textlength(text,font=font)>maxw and font.size>20:
            font=ImageFont.truetype(JP,font.size-2)
    w=d.textlength(text,font=font); d.text((cx-w/2,y),text,font=font,fill=fill); return font.size

def wrap(d,text,font,maxw):
    lines=[];line=""
    for ch in text:
        if d.textlength(line+ch,font=font)>maxw and line:
            lines.append(line);line=ch
        else: line+=ch
    if line:lines.append(line)
    return lines

def type_card(code):
    W=H=1080; d0=LOC[code]; g=BASE[code]["g"]
    img=Image.new("RGB",(W,H),CREAM); img=blobs(img); d=ImageDraw.Draw(img)
    cx=W//2
    # eyebrow pill
    ef=f(30); et="MBTI  ×  恋愛  ×  犬"
    ew=d.textlength(et,font=ef); d.rounded_rectangle([cx-ew/2-30,60,cx+ew/2+30,124],32,fill=PILL)
    d.text((cx-ew/2,78),et,font=ef,fill=PINK)
    # dog image in rounded card with group tint
    DS=520
    card=Image.new("RGB",(DS+48,DS+48),GTINT[g]); img.paste(card,(cx-(DS+48)//2,168),rounded((DS+48,DS+48),46))
    dogp=os.path.join(ROOT,f"{code.lower()}.png")
    if os.path.exists(dogp):
        dog=Image.open(dogp).convert("RGBA"); s=max(DS/dog.width,DS/dog.height)
        dog=dog.resize((int(dog.width*s),int(dog.height*s)))
        l=(dog.width-DS)//2;t=(dog.height-DS)//2; dog=dog.crop((l,t,l+DS,t+DS))
        bg=Image.new("RGBA",(DS,DS),WHITE+(255,)); bg.alpha_composite(dog)
        img.paste(bg.convert("RGB"),(cx-DS//2,192),rounded((DS,DS),38))
    d.rounded_rectangle([cx-(DS+48)//2,168,cx+(DS+48)//2,168+DS+48],46,outline=PINK_BD,width=5)
    y=760
    # breed (big)
    center_text(d,cx,y,d0["breed"],f(72),PINK,maxw=W-140); y+=96
    # code · role
    center_text(d,cx,y,f"{code} ・ {d0['role']}",f(34),INK_SOFT); y+=64
    # tagline (wrap up to 2 lines)
    tf=f(33)
    for ln in wrap(d,d0["tag"],tf,W-160)[:2]:
        center_text(d,cx,y,ln,tf,INK); y+=46
    # footer
    ff=f(30); foot="@16lovetypedogs ・ 16わんこ恋愛診断"
    center_text(d,cx,H-70,foot,ff,INK_SOFT)
    img.save(os.path.join(OUT,f"igcard_{code.lower()}.png"))

def title_card():
    W=H=1080; img=Image.new("RGB",(W,H),CREAM); img=blobs(img); d=ImageDraw.Draw(img); cx=W//2
    ef=f(34); et="MBTI  ×  恋愛  ×  犬"; ew=d.textlength(et,font=ef)
    d.rounded_rectangle([cx-ew/2-30,150,cx+ew/2+30,218],34,fill=PILL); d.text((cx-ew/2,168),et,font=ef,fill=PINK)
    center_text(d,cx,300,"16わんこ",f(150),INK)
    center_text(d,cx,470,"恋愛診断",f(150),PINK)
    center_text(d,cx,560,"",f(20),INK)
    # row of small dogs
    codes=["infp","enfj","enfp","istj"]; x0=cx-2*150+10; ds=150
    for i,c in enumerate(codes):
        p=os.path.join(ROOT,f"{c}.png")
        if os.path.exists(p):
            dg=Image.open(p).convert("RGBA").resize((ds,ds))
            bg=Image.new("RGBA",(ds,ds),WHITE+(255,)); bg.alpha_composite(dg)
            img.paste(bg.convert("RGB"),(x0+i*150,660),rounded((ds,ds),28))
    center_text(d,cx,860,"あなたの恋を、かわいい犬種で診断",f(38),INK)
    center_text(d,cx,930,"12問・無料・登録不要",f(32),INK_SOFT)
    img.save(os.path.join(OUTA,"cover_title.png"))

def cta_card():
    W=H=1080; img=Image.new("RGB",(W,H),CREAM); img=blobs(img); d=ImageDraw.Draw(img); cx=W//2
    center_text(d,cx,200,"あなたは何わんこ？",f(78),INK)
    center_text(d,cx,320,"今すぐ無料で診断",f(56),PINK)
    # center dog image instead of emoji
    p=os.path.join(ROOT,"enfp.png"); ds=300
    if os.path.exists(p):
        dg=Image.open(p).convert("RGBA").resize((ds,ds))
        bg=Image.new("RGBA",(ds,ds),WHITE+(255,)); bg.alpha_composite(dg)
        img.paste(bg.convert("RGB"),(cx-ds//2,440),rounded((ds,ds),60))
        d.rounded_rectangle([cx-ds//2,440,cx+ds//2,440+ds],60,outline=PINK_BD,width=5)
    d.rounded_rectangle([cx-340,800,cx+340,900],50,fill=PINK)
    center_text(d,cx,825,"プロフィールのリンクから",f(40),WHITE)
    center_text(d,cx,950,"@16lovetypedogs",f(38),INK_SOFT)
    img.save(os.path.join(OUTA,"cta_diagnose.png"))

def profile_icon():
    W=H=1080; img=Image.new("RGB",(W,H),CREAM); img=blobs(img); d=ImageDraw.Draw(img); cx=W//2
    p=os.path.join(ROOT,"infp.png")
    if os.path.exists(p):
        ds=560; dg=Image.open(p).convert("RGBA"); s=max(ds/dg.width,ds/dg.height)
        dg=dg.resize((int(dg.width*s),int(dg.height*s))); l=(dg.width-ds)//2;t=(dg.height-ds)//2
        dg=dg.crop((l,t,l+ds,t+ds)); bg=Image.new("RGBA",(ds,ds),WHITE+(255,)); bg.alpha_composite(dg)
        img.paste(bg.convert("RGB"),(cx-ds//2,170),rounded((ds,ds),200))
    center_text(d,cx,760,"16わんこ",f(96),INK)
    center_text(d,cx,880,"恋愛診断",f(96),PINK)
    img.save(os.path.join(OUTA,"profile_icon.png"))

if __name__=="__main__":
    for c in ORDER: type_card(c)
    title_card(); cta_card(); profile_icon()
    print("generated IG assets:",len(ORDER),"type cards + title + cta + icon")
