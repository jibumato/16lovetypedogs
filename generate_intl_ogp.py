#!/usr/bin/env python3
# EN/KO OGPカード(ogp/{en,ko}/*.png)生成。jaと同じポップステッカー調で世界観統一。
# 依存フォント:
#   en → M PLUS Rounded 1c (/tmp/MPLUSRounded1c-{Regular,ExtraBold}.ttf) …ラテン字が丸ゴシックで映える
#   ko → Jua (/tmp/Jua.ttf) …ハングル対応の丸ポップ書体（Google Fonts, 単一ウェイト）
# データ: /tmp/OGP_DATA.json（index.html の LOC/I18N/RARITY と各タイプのベスト相性(best)）
# 使い方: python3 generate_intl_ogp.py [en|ko] [CODE ...]   (langのみ→全16, 引数なし→en,ko全16)
import json, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT=os.path.dirname(os.path.abspath(__file__))
D=json.load(open("/tmp/OGP_DATA.json",encoding="utf-8"))
LOC=D["LOC"];BEST=D.get("best",{});ORDER=D["ORDER"]
MREG="/tmp/MPLUSRounded1c-Regular.ttf";MBOLD="/tmp/MPLUSRounded1c-ExtraBold.ttf";JUA="/tmp/Jua.ttf"
ZCOOL="/tmp/ZCOOL.ttf";IANSUI="/tmp/Iansui.ttf"  # zh=站酷快乐体(丸ポップ簡体), tw=芫荽Iansui(丸繁体)
PINK=(242,145,182);PURPLE=(185,138,232);WHITE=(255,255,255)
INK=(87,79,99);PINK_DEEP=(210,98,143);BOX=(255,253,248)
# 言語別: フォント・箱見出し・ベスト相性ピル・CTA
CFG={
 # sym="font": ― · ▶ をフォント字形で描画（MPLUSは対応）
 # sym="draw": Juaに無い ― · ▶ を図形で描画（ハングル書体は記号非対応）
 "en":{"reg":MREG,"bold":MBOLD,"sym":"font",
       "head":"The Love-Dog Doctor says",
       "role_sep":" · ",
       "pill":lambda b:f"Best match: {b} & more",
       "cta_q":"Which love-dog are you?","site":"16lovetypedogs.com"},
 "ko":{"reg":JUA,"bold":JUA,"sym":"draw",
       "head":"왈왈 박사의 한마디",
       "role_sep":"   ",
       "pill":lambda b:f"베스트 궁합: {b} 등",
       "cta_q":"당신은 어떤 강아지?","site":"16lovetypedogs.com"},
 "zh":{"reg":ZCOOL,"bold":ZCOOL,"sym":"draw",
       "head":"汪汪博士的一句话",
       "role_sep":"   ",
       "pill":lambda b:f"最佳配对：{b} 等",
       "cta_q":"你是哪种恋爱犬？","site":"16lovetypedogs.com"},
 "tw":{"reg":IANSUI,"bold":IANSUI,"sym":"draw",
       "head":"汪汪博士的一句話",
       "role_sep":"   ",
       "pill":lambda b:f"最佳速配：{b} 等",
       "cta_q":"你是哪種戀愛犬？","site":"16lovetypedogs.com"},
}
def make(code,lang):
    cf=CFG[lang]
    def fb(s):return ImageFont.truetype(cf["bold"],s)
    def fr(s):return ImageFont.truetype(cf["reg"],s)
    def wrap(dr,t,f,mw):
        # 空白区切りの語を単位に折り返し（en/ko）。1語が幅を超えたら文字単位で割る
        o=[];ln=""
        for w in t.split(" "):
            cand=(ln+" "+w) if ln else w
            if dr.textlength(cand,font=f)<=mw:ln=cand;continue
            if ln:o.append(ln);ln=""
            if dr.textlength(w,font=f)<=mw:ln=w;continue
            for ch in list(w):
                if dr.textlength(ln+ch,font=f)>mw and ln:o.append(ln);ln=ch
                else:ln+=ch
        if ln:o.append(ln)
        return o
    def fit(dr,t,mk,mw,mn=22):
        s=mk
        while s>mn and dr.textlength(t,font=fb(s))>mw:s-=2
        return fb(s)
    def circle_mask(sz):
        m=Image.new("L",(sz,sz),0);ImageDraw.Draw(m).ellipse([0,0,sz-1,sz-1],fill=255);return m
    def shadow_text(base,xy,text,font,fill=WHITE,anchor="lm"):
        lay=Image.new("RGBA",base.size,(0,0,0,0));ld=ImageDraw.Draw(lay)
        ld.text((xy[0],xy[1]+3),text,font=font,fill=(120,55,95,150),anchor=anchor)
        lay=lay.filter(ImageFilter.GaussianBlur(4));base.alpha_composite(lay)
        ImageDraw.Draw(base).text(xy,text,font=font,fill=fill+(255,),anchor=anchor)
    d=LOC[lang][code];W,H=1200,630
    img=Image.new("RGBA",(W,H),PINK+(255,));dr=ImageDraw.Draw(img)
    dr.polygon([(W,0),(W,H),(0,H)],fill=PURPLE+(255,))
    for k in range(20):
        dr.ellipse([(k*197)%W,(k*271)%H,(k*197)%W+9,(k*271)%H+9],fill=(255,255,255,38))
    # 左：円形ステッカー＋犬
    ccx,ccy,r=300,290,214
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
    bf=fit(dr,d["breed"],50,520,28)
    shadow_text(img,(ccx,ccy+r+50),d["breed"],bf,anchor="mm")
    # code ・ role（· はfont/draw両対応。drawなら白い丸を中央に）
    ry=ccy+r+96
    if cf["sym"]=="draw":
        rf=fr(26);cw=dr.textlength(code,font=rf);rw=dr.textlength(d.get("role",""),font=rf)
        gap=34;tot=cw+gap+rw;sx=ccx-tot/2
        shadow_text(img,(sx,ry),code,rf,anchor="lm")
        shadow_text(img,(sx+cw+gap+rw,ry),d.get("role",""),rf,anchor="rm")
        dcx=sx+cw+gap/2
        ImageDraw.Draw(img).ellipse([dcx-4,ry-4,dcx+4,ry+4],fill=WHITE+(255,))
    else:
        shadow_text(img,(ccx,ry),f"{code} · {d.get('role','')}",fr(26),anchor="mm")
    # 右：コード＋肩書き
    RX=600
    shadow_text(img,(RX,86),code,fb(76),anchor="lm")
    ny=150
    for ln in wrap(dr,d["name"],fb(36),W-RX-40)[:2]:
        shadow_text(img,(RX,ny),ln,fb(36),anchor="lm");ny+=50
    # 博士のひとこと（白箱）… en/ko は hook を使用
    doc=d.get("hook") or d.get("tag","")
    bx1,by1,bx2=RX,ny+16,W-46
    lines=wrap(dr,doc,fr(25),bx2-bx1-40)[:3]
    by2=by1+54+len(lines)*37+16
    dr.rounded_rectangle([bx1,by1,bx2,by2],24,fill=BOX+(255,))
    # 見出し「― わんこ博士のひとこと ―」相当。sym=fontは―字形、drawは棒を描画
    hcx=(bx1+bx2)//2;hy=by1+30
    if cf["sym"]=="draw":
        hf=fit(dr,cf["head"],23,bx2-bx1-120,16)
        dr.text((hcx,hy),cf["head"],font=hf,fill=PINK_DEEP,anchor="mm")
        hw=dr.textlength(cf["head"],font=hf)
        for dx in (-1,1):
            x0=hcx+dx*(hw/2+16);x1=x0+dx*24
            dr.line([min(x0,x1),hy,max(x0,x1),hy],fill=PINK_DEEP,width=4)
    else:
        hf=fit(dr,"― "+cf["head"]+" ―",23,bx2-bx1-40,16)
        dr.text((hcx,hy),"― "+cf["head"]+" ―",font=hf,fill=PINK_DEEP,anchor="mm")
    ty=by1+66
    for ln in lines:dr.text(((bx1+bx2)//2,ty),ln,font=fr(25),fill=INK,anchor="mm");ty+=37
    # ベスト相性ティーザー（ピンクピル）
    bc=BEST.get(code);best_breed=LOC[lang].get(bc,{}).get("breed","") if bc else ""
    if best_breed:
        pt=cf["pill"](best_breed)
        pf=fit(dr,pt,26,W-RX-60,16);pw=int(dr.textlength(pt,font=pf))+44
        py1=by2+18;ph=54
        dr.rounded_rectangle([RX,py1,RX+pw,py1+ph],ph//2,fill=(232,77,128,255))
        dr.text((RX+pw//2,py1+ph//2),pt,font=pf,fill=WHITE,anchor="mm")
    # 巻き込みCTA（下部・白）「{問いかけ} ▶ {site}」。sym=drawは▶を三角で描画
    cy=H-56
    if cf["sym"]=="draw":
        full=cf["cta_q"]+"   "+cf["site"]
        cfont=fit(dr,full,28,W-RX-30,18)
        qw=dr.textlength(cf["cta_q"]+" ",font=cfont)
        shadow_text(img,(RX,cy),cf["cta_q"],cfont,anchor="lm")
        tx=RX+qw+6;th=int(cfont.size*0.5)
        ImageDraw.Draw(img).polygon([(tx,cy-th//2),(tx,cy+th//2),(tx+th*0.85,cy)],fill=WHITE+(255,))
        shadow_text(img,(tx+th+8,cy),cf["site"],cfont,anchor="lm")
    else:
        full=cf["cta_q"]+" ▶ "+cf["site"]
        cfont=fit(dr,full,28,W-RX-30,18)
        shadow_text(img,(RX,cy),full,cfont,anchor="lm")
    return img.convert("RGB")

def gen(lang,codes):
    outdir=os.path.join(ROOT,"ogp",lang);os.makedirs(outdir,exist_ok=True)
    for c in codes: make(c,lang).save(os.path.join(outdir,c.lower()+".png"));print("saved",lang,c)

a=sys.argv[1:]
langs=[a[0]] if a and a[0] in CFG else ["en","ko","zh","tw"]
codes=[x for x in a if x.upper() in ORDER] or ORDER
codes=[c.upper() for c in codes]
for lg in langs: gen(lg,codes)
