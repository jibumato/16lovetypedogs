#!/usr/bin/env python3
"""Generate localized trust pages (about/contact/privacy) for en/zh/ko/tw.

These E-E-A-T pages (operator info, contact, privacy) strengthen domain
trust for international search and AdSense, and complete the footer/nav
clusters. tw content is produced from the zh copy via OpenCC s2tw.
"""
import os, json, html, opencc
ROOT=os.path.dirname(os.path.abspath(__file__))
EMAIL="jbnmatrix@gmail.com"
cc=opencc.OpenCC('s2tw')

STYLE=__import__("re").search(r'<style>(.*?)</style>',
    open(os.path.join(ROOT,"types-en.html"),encoding="utf-8").read(), __import__("re").S).group(1)

CH={
 "en":{"htmllang":"en","locale":"en_US","site":"🐾 16 Love-Type Dogs","quiz":"Take Quiz","types":"Type List",
   "about":"About","contact":"Contact","privacy":"Privacy","home":"Home","types_href":"/types-en.html","suffix":" | 16 Love-Type Dogs",
   "disc":"※Diagnosis results are for entertainment only and are not psychological or medical assessments.<br>※This site uses affiliate links (Amazon Associates) and Google AdSense.<br>© 2025 16 Love-Type Dogs / Mymatrix"},
 "zh":{"htmllang":"zh-CN","locale":"zh_CN","site":"🐾 16恋爱犬测验","quiz":"开始测验","types":"类型一览",
   "about":"关于本站","contact":"联系我们","privacy":"隐私政策","home":"首页","types_href":"/types-zh.html","suffix":"｜16恋爱犬测验",
   "disc":"※诊断结果仅供娱乐，并非心理学或医学诊断。<br>※本站使用联盟链接（Amazon Associates）与 Google AdSense。<br>© 2025 16 Love-Type Dogs / Mymatrix"},
 "ko":{"htmllang":"ko","locale":"ko_KR","site":"🐾 16 연애견 진단","quiz":"진단하기","types":"유형 목록",
   "about":"운영자 정보","contact":"문의하기","privacy":"개인정보처리방침","home":"홈","types_href":"/types-ko.html","suffix":"｜16 연애견 진단",
   "disc":"※진단 결과는 오락용이며 심리학적·의학적 진단이 아닙니다.<br>※본 사이트는 제휴 링크(Amazon Associates)와 Google AdSense를 사용합니다.<br>© 2025 16 Love-Type Dogs / Mymatrix"},
}
LANG_LABEL={"ja":"日本語","en":"English","ko":"한국어","zh":"简体中文","tw":"繁體中文"}
# native page slugs per page-type per lang
def slug(ptype,lang):
    if lang=="ja": return f"{ptype}.html"
    return f"{ptype}-{lang}.html"

# ---- content (en/zh/ko authored; tw via opencc from zh) ----
ABOUT={
 "en":{"title":"About","sub":"About 16 Love-Type Dogs",
   "sec":[("About this site","\"16 Love-Type Dogs\" is a site that, based on MBTI theory, likens 16 love styles to cute dog breeds. Answer just 12 questions to analyze your love style and get your most compatible types and daily love advice. Results are for entertainment only and are not psychological or medical assessments — please enjoy them lightly."),
     ("Operator","Trade name: Mymatrix<br>Representative: Private (individually operated)<br>Location: Nagoya, Aichi, Japan<br>Contact: <a href=\"/contact-en.html\">Contact form</a>"),
     ("Basis &amp; reference","The diagnosis axes reference the four MBTI (Myers–Briggs Type Indicator) axes (E/I, S/N, T/F, J/P). This site is not officially licensed by MBTI® and is original entertainment content built around the MBTI theme."),
     ("Ads &amp; affiliates","This site uses Google AdSense ads and affiliate links via the Amazon Associates Program. See our <a href=\"/privacy-en.html\">privacy policy</a> for details.")]},
 "zh":{"title":"关于本站","sub":"关于「16恋爱犬测验」",
   "sec":[("关于本站","「16恋爱犬测验」是一个以MBTI理论为基础、把16种恋爱类型比作可爱犬种来诊断的网站。只需回答12道题，就能分析你的恋爱风格，并为你呈现契合的类型与今日恋爱建议。诊断结果仅供娱乐，并非心理学或医学诊断，请轻松享受。"),
     ("运营者","商号：Mymatrix<br>负责人：不公开（个人运营）<br>所在地：日本爱知县名古屋市<br>联系方式：<a href=\"/contact-zh.html\">联系表单</a>"),
     ("依据与参考","诊断轴参考MBTI（Myers–Briggs Type Indicator）的四个维度（E/I・S/N・T/F・J/P）。本站并非MBTI®官方授权，而是以MBTI为题材的原创娱乐内容。"),
     ("广告与联盟","本站使用 Google AdSense 广告与 Amazon 联盟计划的推广链接。详情请见<a href=\"/privacy-zh.html\">隐私政策</a>。")]},
 "ko":{"title":"운영자 정보","sub":"「16 연애견 진단」 소개",
   "sec":[("사이트 소개","「16 연애견 진단」은 MBTI 이론을 바탕으로 16가지 연애 유형을 귀여운 견종에 빗대어 진단하는 사이트입니다. 12개의 질문에 답하기만 하면 당신의 연애 스타일을 분석하고, 잘 맞는 유형과 오늘의 연애 조언을 알려드립니다. 진단 결과는 오락용이며 심리학적·의학적 진단이 아니니 가볍게 즐겨 주세요."),
     ("운영자","상호: Mymatrix<br>대표: 비공개(개인 운영)<br>소재지: 일본 아이치현 나고야시<br>문의: <a href=\"/contact-ko.html\">문의 양식</a>"),
     ("근거 및 참고","진단 축은 MBTI(Myers–Briggs Type Indicator)의 네 가지 축(E/I·S/N·T/F·J/P)을 참고합니다. 본 사이트는 MBTI® 공식 라이선스를 받지 않았으며, MBTI를 소재로 한 독자적인 오락 콘텐츠입니다."),
     ("광고 및 제휴","본 사이트는 Google AdSense 광고와 Amazon 어소시에이트 프로그램의 제휴 링크를 사용합니다. 자세한 내용은 <a href=\"/privacy-ko.html\">개인정보처리방침</a>을 참고하세요.")]},
}
CONTACT={
 "en":{"title":"Contact","sub":"Feedback, requests and bug reports welcome",
   "sec":[("How to contact us",f"Feel free to email us at the address below. Depending on the content, a reply may take some time.<br><br>📧 <a href=\"mailto:{EMAIL}\">{EMAIL}</a>"),
     ("Examples of inquiries","・Feedback or requests about results and content<br>・Bug or display issue reports<br>・Copyright or content inquiries<br>・Advertising or affiliate inquiries<br>・Media or interview requests<br><br>※We do not provide fortune-telling interpretations of results or answer individual relationship consultations.<br>※We do not reply to spam or sales emails.")]},
 "zh":{"title":"联系我们","sub":"欢迎提出意见、需求与故障反馈",
   "sec":[("联系方式",f"请随时通过以下邮箱与我们联系。视内容而定，回复可能需要一些时间。<br><br>📧 <a href=\"mailto:{EMAIL}\">{EMAIL}</a>"),
     ("咨询内容示例","・对诊断结果与内容的意见或需求<br>・显示故障、Bug 反馈<br>・版权或内容相关咨询<br>・广告或联盟相关咨询<br>・媒体报道或采访邀约<br><br>※本站不提供对结果的占卜式解读，也不回答个别的恋爱咨询。<br>※不回复垃圾邮件或推销邮件。")]},
 "ko":{"title":"문의하기","sub":"의견·요청·오류 제보를 환영합니다",
   "sec":[("문의 방법",f"아래 이메일로 편하게 연락해 주세요. 내용에 따라 답변에 시간이 걸릴 수 있습니다.<br><br>📧 <a href=\"mailto:{EMAIL}\">{EMAIL}</a>"),
     ("문의 내용 예시","・진단 결과·콘텐츠에 대한 의견이나 요청<br>・표시 오류·버그 제보<br>・저작권·콘텐츠 관련 문의<br>・광고·제휴 관련 문의<br>・미디어 게재·취재 의뢰<br><br>※진단 결과에 대한 점술적 해석이나 개별 연애 상담에는 답변하지 않습니다.<br>※스팸·영업 메일에는 답장하지 않습니다.")]},
}
# privacy: reuse English sections (from privacy-en) translated to zh/ko
PRIVACY={
 "zh":{"title":"隐私政策","sub":"最后更新：2025",
   "sec":[("1. 运营者",f"本站「16恋爱犬测验」由 Mymatrix 运营（联系方式：{EMAIL}）。"),
     ("2. 访问分析","本站使用 Google Analytics，通过 cookie 收集匿名访问数据（页面浏览量、停留时间、设备类型等）。详情请见 <a href=\"https://policies.google.com/technologies/partner-sites\" target=\"_blank\" rel=\"noopener\">Google 隐私政策</a>。"),
     ("3. 本地存储","为提升使用体验，本站可能在你的浏览器本地存储中保存图鉴、每日运势等数据。这些数据不会发送到任何服务器，可随时在浏览器设置中删除。"),
     ("4. Google AdSense","本站通过 Google AdSense 显示广告。Google 可能使用 cookie，根据你的浏览记录展示个性化广告。你可在 <a href=\"https://adssettings.google.com/\" target=\"_blank\" rel=\"noopener\">Google 广告设置</a> 中关闭。详情见 <a href=\"https://policies.google.com/technologies/ads\" target=\"_blank\" rel=\"noopener\">Google 广告政策</a>。"),
     ("5. Amazon 联盟","本站参与 Amazon 联盟计划。当你通过本站链接购买时，我们可能获得推广佣金，你无需支付额外费用。"),
     ("6. 第三方披露","除法律要求外，我们不会向第三方提供个人信息。"),
     ("7. 免责声明","本站内容仅供娱乐。诊断结果并非心理学或医学诊断。对于因使用本站而产生的任何损害，我们不承担责任。"),
     ("8. 联系","隐私相关咨询请通过<a href=\"/contact-zh.html\">联系页面</a>。")]},
 "ko":{"title":"개인정보처리방침","sub":"최종 업데이트: 2025",
   "sec":[("1. 운영자",f"본 사이트 「16 연애견 진단」은 Mymatrix가 운영합니다(연락처: {EMAIL})."),
     ("2. 접속 분석","본 사이트는 Google Analytics를 사용하여 cookie를 통해 익명 접속 데이터(페이지뷰, 체류 시간, 기기 유형 등)를 수집합니다. 자세한 내용은 <a href=\"https://policies.google.com/technologies/partner-sites\" target=\"_blank\" rel=\"noopener\">Google 개인정보처리방침</a>을 참고하세요."),
     ("3. 로컬 스토리지","사용성 향상을 위해 본 사이트는 도감, 오늘의 운세 결과 등의 데이터를 브라우저 로컬 스토리지에 저장할 수 있습니다. 이 데이터는 서버로 전송되지 않으며 언제든 브라우저 설정에서 삭제할 수 있습니다."),
     ("4. Google AdSense","본 사이트는 Google AdSense를 통해 광고를 표시합니다. Google은 cookie를 사용하여 열람 기록을 바탕으로 맞춤 광고를 표시할 수 있습니다. <a href=\"https://adssettings.google.com/\" target=\"_blank\" rel=\"noopener\">Google 광고 설정</a>에서 해제할 수 있습니다. 자세한 내용은 <a href=\"https://policies.google.com/technologies/ads\" target=\"_blank\" rel=\"noopener\">Google 광고 정책</a>을 참고하세요."),
     ("5. Amazon 어소시에이트","본 사이트는 Amazon 어소시에이트 프로그램에 참여합니다. 본 사이트 링크를 통해 구매하시면 추천 수수료를 받을 수 있으며, 추가 비용은 발생하지 않습니다."),
     ("6. 제3자 제공","법령에 의한 경우를 제외하고 개인정보를 제3자에게 제공하지 않습니다."),
     ("7. 면책 조항","본 사이트의 콘텐츠는 오락 목적입니다. 진단 결과는 심리학적·의학적 진단이 아닙니다. 본 사이트 이용으로 발생한 손해에 대해 책임지지 않습니다."),
     ("8. 문의","개인정보 관련 문의는 <a href=\"/contact-ko.html\">문의 페이지</a>를 이용해 주세요.")]},
}

def esc(s): return s  # content already HTML-safe (intentional inline tags)

def langbar(ptype, cur):
    out=[]
    for lg in ["ja","en","ko","zh","tw"]:
        lab=LANG_LABEL[lg]
        if lg==cur:
            out.append(f'<span style="font-size:12.5px;font-weight:800;color:#fff;background:var(--pink-deep);border:2px solid var(--pink-deep);border-radius:999px;padding:5px 13px">{lab}</span>')
        else:
            out.append(f'<a href="/{slug(ptype,lg)}" style="font-size:12.5px;font-weight:700;color:var(--ink-soft);background:#fff;border:2px solid var(--beige);border-radius:999px;padding:5px 13px;text-decoration:none">{lab}</a>')
    return '<div class="langbar" style="display:flex;justify-content:center;gap:6px;padding:12px 0;flex-wrap:wrap">'+"".join(out)+'</div>'

def hreflang(ptype):
    b="https://16lovetypedogs.com/"
    return "\n".join([
      f'<link rel="alternate" hreflang="ja" href="{b}{slug(ptype,"ja")}">',
      f'<link rel="alternate" hreflang="en" href="{b}{slug(ptype,"en")}">',
      f'<link rel="alternate" hreflang="ko" href="{b}{slug(ptype,"ko")}">',
      f'<link rel="alternate" hreflang="zh-Hans" href="{b}{slug(ptype,"zh")}">',
      f'<link rel="alternate" hreflang="zh-Hant" href="{b}{slug(ptype,"tw")}">',
      f'<link rel="alternate" hreflang="x-default" href="{b}{slug(ptype,"en")}">',
    ])

TPL="""<!DOCTYPE html>
<html lang="{htmllang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}{suffix}</title>
<meta name="description" content="{sub}">
<meta property="og:type" content="website">
<meta property="og:locale" content="{locale}">
<meta property="og:title" content="{title}{suffix}">
<meta property="og:description" content="{sub}">
<meta property="og:url" content="https://16lovetypedogs.com/{self_path}">
<meta property="og:image" content="https://16lovetypedogs.com/ogp.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index,follow">
<link rel="canonical" href="https://16lovetypedogs.com/{self_path}">
{hreflang}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c:wght@400;500;700;800&family=Baloo+2:wght@500;700;800&family=Zen+Maru+Gothic:wght@500;700&display=swap" rel="stylesheet">
<style>{style}</style>
</head><body>
<header>
  <div class="hinner">
    <a class="site-logo" href="/">{site}</a>
    <nav>
      <a href="/">{quiz}</a>
      <a href="{types_href}">{types}</a>
      <a href="/{about_slug}">{about}</a>
      <a href="/{privacy_slug}">{privacy}</a>
    </nav>
  </div>
</header><div class="wrap">{langbar}
  <div class="breadcrumb"><a href="/">{home}</a> › {title}</div>
  <div class="hero"><h1 style="font-size:clamp(20px,5vw,24px);font-weight:800;color:var(--pink-deep)">{title}</h1><p class="sub">{sub}</p></div>
  {cards}
</div>
<footer>
  <div style="margin-bottom:8px"><a href="/">{quiz}</a> ｜ <a href="{types_href}">{types}</a> ｜ <a href="/{about_slug}">{about}</a> ｜ <a href="/{contact_slug}">{contact}</a> ｜ <a href="/{privacy_slug}">{privacy}</a></div>
  {disc}
</footer>
</body></html>
"""

def card(h,b):
    return (f'<div class="card"><h2 style="font-size:17px;font-weight:800;color:var(--pink-deep);'
            f'margin-bottom:10px;padding-bottom:8px;border-bottom:2px solid var(--beige)">{h}</h2><p>{b}</p></div>')

def render(ptype, lang, data):
    c=CH[lang]
    cards="".join(card(h,b) for h,b in data["sec"])
    out=TPL.format(htmllang=c["htmllang"],locale=c["locale"],title=data["title"],suffix=c["suffix"],sub=data["sub"],
        self_path=slug(ptype,lang),hreflang=hreflang(ptype),style=STYLE,site=c["site"],quiz=c["quiz"],
        types=c["types"],types_href=c["types_href"],about=c["about"],privacy=c["privacy"],contact=c["contact"],
        home=c["home"],langbar=langbar(ptype,lang),cards=cards,disc=c["disc"],
        about_slug=slug("about",lang),privacy_slug=slug("privacy",lang),contact_slug=slug("contact",lang))
    open(os.path.join(ROOT,slug(ptype,lang)),"w",encoding="utf-8").write(out)

def tw_from_zh(data):
    return {"title":cc.convert(data["title"]),"sub":cc.convert(data["sub"]),
            "sec":[(cc.convert(h),cc.convert(b)) for h,b in data["sec"]]}

# add tw chrome by converting zh chrome
CH["tw"]=dict(CH["zh"]); CH["tw"].update({"htmllang":"zh-TW","locale":"zh_TW","site":"🐾 16戀愛犬測驗",
  "quiz":cc.convert(CH["zh"]["quiz"]),"types":cc.convert(CH["zh"]["types"]),"about":cc.convert(CH["zh"]["about"]),
  "contact":cc.convert(CH["zh"]["contact"]),"privacy":cc.convert(CH["zh"]["privacy"]),"home":cc.convert(CH["zh"]["home"]),
  "types_href":"/types-tw.html","suffix":"｜16戀愛犬測驗",
  "disc":cc.convert(CH["zh"]["disc"])})

if __name__=="__main__":
    n=0
    for lang in ["en","zh","ko"]:
        render("about",lang,ABOUT[lang]); n+=1
        render("contact",lang,CONTACT[lang]); n+=1
    for lang in ["zh","ko"]:
        render("privacy",lang,PRIVACY[lang]); n+=1
    # tw via opencc from zh
    render("about","tw",tw_from_zh(ABOUT["zh"])); n+=1
    render("contact","tw",tw_from_zh(CONTACT["zh"])); n+=1
    render("privacy","tw",tw_from_zh(PRIVACY["zh"])); n+=1
    print(f"generated {n} intl trust pages")
