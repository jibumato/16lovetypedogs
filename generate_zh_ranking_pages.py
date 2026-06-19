#!/usr/bin/env python3
"""Generate the 5 Simplified-Chinese ranking pages (ranking-*-zh.html).

Mirrors generate_en_ranking_pages.py: ranking order parsed from the JA
source pages, breed/type names from LOC['zh'], stars from STARS, and all
80 per-rank blurbs translated to natural Simplified Chinese here.
"""
import re, os, json, html
ROOT=os.path.dirname(os.path.abspath(__file__))
src=open(os.path.join(ROOT,"index.html"),encoding="utf-8").read()
LOC=json.loads(re.search(r'\nconst LOC=(\{.*?\});\n',src,re.DOTALL).group(1))
ZH=LOC["zh"]

STARS={
 'loyalty':{'INTJ':5,'INTP':4,'ENTJ':4,'ENTP':2,'INFJ':5,'INFP':5,'ENFJ':4,'ENFP':3,'ISTJ':5,'ISFJ':5,'ESTJ':4,'ESFJ':4,'ISTP':3,'ISFP':3,'ESTP':2,'ESFP':3},
 'devotion':{'INTJ':3,'INTP':2,'ENTJ':4,'ENTP':2,'INFJ':4,'INFP':4,'ENFJ':5,'ENFP':4,'ISTJ':3,'ISFJ':5,'ESTJ':4,'ESFJ':5,'ISTP':2,'ISFP':3,'ESTP':3,'ESFP':4},
 'marriage':{'INTJ':4,'INTP':2,'ENTJ':4,'ENTP':2,'INFJ':4,'INFP':3,'ENFJ':4,'ENFP':2,'ISTJ':5,'ISFJ':5,'ESTJ':5,'ESFJ':4,'ISTP':2,'ISFP':3,'ESTP':2,'ESFP':3},
 'jealousy':{'INTJ':4,'INTP':1,'ENTJ':3,'ENTP':2,'INFJ':3,'INFP':3,'ENFJ':3,'ENFP':4,'ISTJ':2,'ISFJ':3,'ESTJ':3,'ESFJ':5,'ISTP':2,'ISFP':2,'ESTP':3,'ESFP':5},
 'dokidoki':{'INTJ':2,'INTP':2,'ENTJ':3,'ENTP':5,'INFJ':2,'INFP':3,'ENFJ':3,'ENFP':5,'ISTJ':1,'ISFJ':1,'ESTJ':2,'ESFJ':3,'ISTP':3,'ISFP':3,'ESTP':5,'ESFP':5},
}
def stars(n): return "★"*n+"☆"*(5-n)

META={
 "loyalty":{"ja":"ranking-loyalty.html","title":"最专一的MBTI排行榜TOP16｜不会变心的恋爱类型是谁？【用犬种看懂】",
   "sub":"一旦爱上就一心一意，绝缘出轨的「专一狗狗」是谁？",
   "intro":"「一旦喜欢上一个人，那个人就是全部。」你有多专一，和性格类型大有关系。这份排行榜把MBTI的16种类型比作犬种，按恋爱中的专一程度从高到低排列，你的类型也许会让你意外。"},
 "marriage":{"ja":"ranking-marriage.html","title":"最适合结婚的MBTI排行榜TOP16｜和谁结婚最幸福？【用犬种看懂】",
   "sub":"踏实、可靠又温暖——哪些狗狗天生适合走进婚姻？",
   "intro":"「适合谈恋爱」和「适合结婚」并不总是同一回事。你有多适合建立稳定的家庭，和性格类型大有关系。这份排行榜把MBTI的16种类型比作犬种，按结婚适合度从高到低排列。"},
 "jealousy":{"ja":"ranking-jealousy.html","title":"最爱吃醋的MBTI排行榜TOP16｜占有欲最强的恋爱类型是谁？【用犬种看懂】",
   "sub":"一点点醋意也很可爱——但谁吃醋吃得最凶？",
   "intro":"会吃醋，正是因为在乎。但表现得有多明显，和性格类型大有关系。这份排行榜把MBTI的16种类型比作犬种，按恋爱中的吃醋程度从高到低排列。"},
 "devotion":{"ja":"ranking-devotion.html","title":"最会付出的MBTI排行榜TOP16｜深情奉献的恋爱类型是谁？【用犬种看懂】",
   "sub":"满满的关怀与用心——哪些狗狗最懂得为爱付出？",
   "intro":"有些人就是忍不住想为喜欢的人付出。你在恋爱里有多愿意奉献，和性格类型大有关系。这份排行榜把MBTI的16种类型比作犬种，按付出程度从高到低排列。"},
 "dokidoki":{"ja":"ranking-dokidoki.html","title":"最让人心动的MBTI排行榜TOP16｜恋爱最刺激的类型是谁？【用犬种看懂】",
   "sub":"永远不无聊——哪些狗狗能让你一直心跳加速？",
   "intro":"有些人能让你每天都心跳加速。你能带来多少心动，和性格类型大有关系。这份排行榜把MBTI的16种类型比作犬种，按心动程度从高到低排列。"},
}

TX={
 "loyalty":{
  "INTJ":"警惕心强的吉娃娃，要敞开心扉需要时间，但一旦认定「就是这个人」，专一程度毋庸置疑，几乎不会对本命以外的人动心。",
  "INFJ":"骑士查理王是相信「命中注定那一个」的深爱型。正因为不轻易喜欢上别人，对选定的对象便会倾尽所有去爱。",
  "INFP":"梦想理想之恋的马尔济斯，会把喜欢的人长久地放在心里的特等席上。情感的深度与持久力都是顶级。",
  "ISTJ":"柴犬是恋爱界的匠人。不张扬，却会把一旦认定的对象一生珍惜到底，是古典而坚定的专一派。",
  "ISFJ":"西施犬是默默陪伴所爱之人的奉献型。心意很少动摇，会用漫长的时间持续爱着同一个人。",
  "INTP":"雪纳瑞看似对恋爱很淡，其实一旦沦陷就是深度钻研型。对触动了开关的对象，兴趣会持续很久。",
  "ENTJ":"柯基是认定「就是这个人」就会全力守护的领袖型。虽然喜欢掌握恋爱主导权，但变心的可能性很低。",
  "ENFJ":"黄金猎犬虽然社交又受欢迎，对本命的忠诚却很强。对谁都温柔，但心的正中央只属于一个人。",
  "ESTJ":"波士顿梗是着眼未来、诚实相待的踏实派。不喜欢暧昧或轻浮的恋爱，认定一人便心无旁骛。",
  "ESFJ":"拉布拉多是充满爱意又爱照顾人的类型。虽有怕寂寞的一面，但对所爱之人的心意笔直而真诚。",
  "ENFP":"贵宾犬看似善变，本质却很专一。对敞开心扉的对象，会笔直地持续倾注热闹的爱意。",
  "ISTP":"腊肠犬冷静、执着心也淡。但对信任的人，那份不说出口的安静忠诚确实存在。",
  "ISFP":"法斗是我行我素的自由派，但和相处舒服的人会长久而平和地走下去。不激烈，却很稳定。",
  "ESFP":"博美想当恋爱里的主角、渴望被爱。在感受到被爱时很专一，一旦被冷落就容易不安。",
  "ENTP":"杰克罗素是恋爱猎人气质。追逐时最炽热，进入稳定期后可能又想去寻找新的刺激。",
  "ESTP":"比格犬是追求刺激的行动派。心意坦率直接，但在无聊的关系里热度容易冷却。",
 },
 "devotion":{
  "ENFJ":"付出度第一名是黄金猎犬。对方的幸福就是自己的幸福，纪念日和细微体贴都做得完美。只是常常付出过头而忽略自己，记得把爱回馈给它。",
  "ISFJ":"西施犬是「不动声色」付出的高手。不等你开口就先察觉行动，是能挠到痒处的奉献派。",
  "ESFJ":"拉布拉多表达爱意直接又毫不吝啬。勤快的联系、亲手做的料理、惊喜——满满地给你被爱的实感。",
  "ENTJ":"柯基是用行动付出的派别：守护、支持、引领。遇到难题时,它是最靠得住的那一个。",
  "INFJ":"骑士查理王是连没说出口的心情都能体察的细腻付出型。照顾人心的能力一流。",
  "INFP":"马尔济斯是为了喜欢的人就会自然努力的纯粹奉献家。不求回报的爱法正是它的魅力。",
  "ENFP":"贵宾犬是用「一起玩乐」来灌注爱的类型。策划惊喜和活动的本事无人能及。",
  "ESTJ":"波士顿梗是用稳定与计划付出的务实派。不花哨，但支撑生活的力量货真价实。",
  "ESFP":"博美既喜欢被爱，也超爱逗所爱之人开心。连反应都很到位，付出得活泼又有趣。",
  "INTJ":"吉娃娃是本命限定的付出型。在外不展露的撒娇宠溺，只在两人独处时才会开启。",
  "ISTJ":"柴犬即使嘴笨，也会用行动表达。守约、守时——这些点滴的积累就是它的爱意表达。",
  "ISFP":"法斗光是陪在身边就能治愈你。它的付出不在于「做」什么，而在于「有它在」。",
  "ESTP":"比格犬是带来欢乐体验的娱乐型。情绪低落的日子,把你拉出门的就是这一型。",
  "INTP":"雪纳瑞虽然笨拙,却比谁都记得你的喜好,是观察型。偶尔的一句话能深深戳中你。",
  "ENTP":"杰克罗素与其说付出,不如说更擅长逗你开心。它给的是另一种礼物:永不无聊的每一天。",
  "ISTP":"腊肠犬平时显得冷淡,但你真正陷入困境时会默默出手——是「关键时刻」型的付出。",
 },
 "marriage":{
  "ISTJ":"柴犬守约、一点一滴积累信任,是务实派。不忘纪念日,家计与生活都有计划。堪称「结婚让人安心」的代表。",
  "ISFJ":"西施犬位居结婚适合度之巅。不着痕迹的体贴、奉献与安定感三者兼备,会成为温暖支撑日常生活的伴侣。",
  "ESTJ":"波士顿梗能把家庭这支「团队」经营得井井有条。责任感强,是守护家人的顶梁柱气质。",
  "INTJ":"吉娃娃会把婚姻当作「人生战略」认真考量。决定前很谨慎,但定下来之后的安定感无可挑剔。",
  "ENTJ":"柯基连家庭的未来规划都会牢牢主导,可靠又能干。即使双薪也不会让你一人扛,计划性十足。",
  "INFJ":"骑士查理王是能建立深刻精神连结的终身伴侣。不张扬,却能营造心意相通的家庭。",
  "ENFJ":"黄金猎犬把家人的幸福当作自己的幸福,是奉献型。会成为温暖家庭中心、太阳般的存在。",
  "ESFJ":"拉布拉多是重视家庭活动、爱意丰沛的类型。会营造热闹又温暖的家。",
  "INFP":"马尔济斯会把理想与温柔带进家庭,是浪漫主义者。和能让它安心的人,能建立深厚羁绊的家庭。",
  "ISFP":"法斗偏好平稳无争的家庭,是和平主义者。家里会是节奏舒缓、住起来很舒服的地方。",
  "ESFP":"博美是让家变得明亮的气氛担当。能把每天过得开心,但家务的计划性若有伴侣协助会更好。",
  "INTP":"雪纳瑞比起生活琐事更看重知性世界。和能把家务分工制度化的对象在一起会很舒适。",
  "ENTP":"杰克罗素是热爱自由与刺激的冒险家。比起按部就班的婚姻样板,更需要能一起打造「专属两人」形式的对象。",
  "ENFP":"贵宾犬即使结了婚也不想丢掉恋人般的心情。和能一起对抗一成不变的对象在一起才能长久。",
  "ISTP":"腊肠犬偏好互不过度干涉、各自独立的夫妻关系。不黏腻的成熟婚姻生活最适合它。",
  "ESTP":"比格犬是家里的玩乐与活动担当。靠干劲和行动力为家庭制造惊喜,沉稳安定则还有待修炼。",
 },
 "jealousy":{
  "ESFJ":"拉布拉多是「希望被同等回应」的类型。一旦觉得回来的爱意变淡,吃醋与寂寞就会浮现。",
  "ESFP":"堂堂第一名是博美。渴望被关注、被宠爱,所以当恋人的注意力转向别处,就会浑身坐立不安。那种一目了然的醋意也是一种可爱。",
  "INTJ":"意外的高名次是吉娃娃。表面冷酷,内心的占有欲却在悄悄滋长。因为不说出口,反而容易越积越多。",
  "ENFP":"贵宾犬热闹又自由,其实很怕寂寞。当恋人的联系变少就会不安,容易吃起醋来。",
  "ENTJ":"柯基的占有欲带着不服输。情敌出现时,与其吃醋,不如说更会用「斗志」去正面对抗。",
  "INFJ":"骑士查理王是「希望只看着我」的深爱型。平时会忍耐,一旦超过极限便会安静地满溢出来。",
  "INFP":"马尔济斯因为情感深,不安也容易滋长。说不出口,常常一个人偷偷受伤。",
  "ENFJ":"黄金猎犬会把「对方的幸福」摆在自己的吃醋之上,是无私的爱。反而要担心它忍得太多。",
  "ISFJ":"西施犬即使吃醋也不表露,默默忍耐,是体贴到让人心疼的类型。你能不能察觉就是关键。",
  "ESTJ":"波士顿梗会在觉得伴侣的行为「不合情理」时心生不快。与其说是吃醋,不如说是秩序的问题。",
  "ESTP":"比格犬性子干脆不记仇。就算一瞬间不爽,一有好玩的事马上就忘。",
  "ENTP":"杰克罗素喜欢追逐,吃醋更像在玩游戏。情敌的存在甚至会成为燃料。",
  "ISTJ":"柴犬是以信任为前提相处的硬派。本就不擅长怀疑,会用真诚而非醋意守护关系。",
  "ISTP":"腊肠犬是执着心淡薄的冷静代表。不喜欢束缚也不爱吃醋,向往自由与信任的关系。",
  "ISFP":"法斗是平和的和平主义者。多数事都能用「算了吧」一笑带过,是少吃醋的类型。",
  "INTP":"雪纳瑞觉得吃醋「不理性」,会用理智去面对。并非不在意,而是分析后再消化掉。",
 },
 "dokidoki":{
  "ENTP":"心动度第一名是杰克罗素梗。机智的谈吐、难以预料的行动力、绝妙的进退拉扯——能谈一场字典里没有「无聊」二字的恋爱。",
  "ENFP":"贵宾犬是好奇心与热情的集合体。新游戏、新地方、丰沛的情绪反应,让心动持续不断。",
  "ESTP":"比格犬是一有念头就立刻行动的刺激制造机。「现在就去海边吧」真的会成行,是充满现场感的恋爱。",
  "ESFP":"博美是把每天都点亮成主角级的娱乐家。光是在一起,恋爱就充满活动般的雀跃。",
  "ENTJ":"柯基带来被强力牵引的心动感。决断之快与可靠,会冷不防地让你心跳。",
  "INFP":"马尔济斯用浪漫的世界观让你心动。情书、纪念日的用心安排,创造留在心里的瞬间。",
  "ENFJ":"黄金猎犬是王道的心动供给型。擅长照顾陪伴,把被珍惜的实感化作怦然心动。",
  "ESFJ":"拉布拉多用直接的爱意表达让你心头一颤。毫不吝啬地说「喜欢」的坦率,正是它的武器。",
  "ISTP":"腊肠犬平时冷酷,却会用关键时刻的可靠把你拿下,是慢热型的心动。",
  "ISFP":"法斗会在平静之中,因一抹不经意流露的真我而让你心动。后劲慢慢上来。",
  "INTJ":"吉娃娃靠冷酷转撒娇的反差取胜。偶尔露出的依赖,会一箭射穿你的心脏。",
  "INTP":"雪纳瑞的魅力,是给你一个没人察觉到的视角,那份知性灵光。对喜欢聪明人的人特别有效。",
  "INFJ":"骑士查理王会在深度对话拉近心灵距离的瞬间让你心动,是精神层面的怦然。",
  "ESTJ":"波士顿梗以安定感见长,心动则较为克制。换来的是一段不必担心被背叛的恋爱。",
  "ISTJ":"柴犬是重信任胜过刺激的人。心动也许少一些,却给你最强的根基:长久的安心。",
  "ISFJ":"西施犬的心动总和「安心」成对出现。一抹不经意的温柔,会让你的心暖暖地动一下。",
 },
}

CHROME={"htmllang":"zh-CN","locale":"zh_CN","suffix":"｜16恋爱犬测验","site":"🐾 16恋爱犬测验",
  "quiz":"开始测验","types":"类型一览","privacy":"隐私政策","cta":"🐶 开始测验","ranking":"排行榜",
  "related":"相关文章","reference":"仅供参考。基于「16恋爱犬测验」的恋爱属性，仅作娱乐用途。",
  "types_href":"/types-zh.html","privacy_href":"/privacy.html","profile":"查看完整档案",
  "disc":"※排行榜与诊断结果仅供娱乐，并非心理学或医学诊断。<br>※本站使用联盟链接（Amazon Associates）与 Google AdSense。<br>© 2025 16 Love-Type Dogs / Mymatrix"}
REL_LABEL={"loyalty":"最专一的MBTI排行榜TOP16","marriage":"最适合结婚的MBTI排行榜TOP16",
  "jealousy":"最爱吃醋的MBTI排行榜TOP16","devotion":"最会付出的MBTI排行榜TOP16","dokidoki":"最让人心动的MBTI排行榜TOP16"}
ALL=["loyalty","marriage","jealousy","devotion","dokidoki"]
LANG="zh"

def esc(s): return html.escape(s,quote=True)
def parse_order(ja_file):
    s=open(os.path.join(ROOT,ja_file),encoding="utf-8").read()
    items=re.findall(r'(?:<div class="medal"[^>]*>([^<]*)</div>|<div class="no"[^>]*>([0-9]+)</div>).*?src="/([a-z]{4})\.webp"', s, re.DOTALL)
    out=[]
    for med,no,code in items:
        if med:
            rank={"🥇":1,"🥈":2,"🥉":3}.get(med.strip(),1)
            marker=f'<div class="medal" style="font-size:24px">{med.strip()}</div>'
        else:
            rank=int(no); marker=f'<div class="no" style="font-family:Baloo 2;font-weight:800;font-size:20px;color:var(--pink-deep)">{no}</div>'
        out.append((rank,marker,code.upper()))
    return out

def rank_items(metric):
    blocks=""
    for rank,marker,code in parse_order(META[metric]["ja"]):
        breed=esc(ZH[code]["breed"]); name=esc(ZH[code]["name"]); c=code.lower()
        blocks+=(f'<div class="rankitem">\n'
          f'  <div class="rk">{marker}<img loading="lazy" decoding="async" src="/{c}.webp" alt="{breed}" style="width:54px;height:auto;border-radius:12px;margin-top:4px" onerror="this.style.display=\'none\'"></div>\n'
          f'  <div class="rbody">\n    <div class="nm">#{rank} {breed}（{code}）</div>\n'
          f'    <div class="bd">{name}</div>\n'
          f'    <div class="st" style="color:#c79a3f;font-size:14px;letter-spacing:1.5px">{stars(STARS[metric][code])}</div>\n'
          f'    <p class="tx" style="font-size:13.5px;line-height:1.8;margin-top:5px">{esc(TX[metric][code])}</p>\n'
          f'    <a href="/type-{c}-{LANG}.html" style="font-size:12px;font-weight:700">→ {CHROME["profile"]} {breed}</a>\n'
          f'  </div>\n</div>')
    return blocks

def related(metric):
    out=""
    for m in ALL:
        if m==metric: continue
        out+=(f'<a href="/ranking-{m}-{LANG}.html" style="display:block;background:var(--bg);border:1.5px solid var(--beige);'
              f'border-radius:12px;padding:10px 14px;font-size:13px;font-weight:700;text-decoration:none">{REL_LABEL[m]}</a>')
    out+=(f'<a href="{CHROME["types_href"]}" style="display:block;background:var(--bg);border:1.5px solid var(--beige);'
          f'border-radius:12px;padding:10px 14px;font-size:13px;font-weight:700;text-decoration:none">{CHROME["types"]}</a>')
    return out

def langbar(metric):
    return ('<div class="langbar" style="display:flex;justify-content:center;gap:6px;padding:12px 0;flex-wrap:wrap">'
      f'<a href="ranking-{metric}.html" style="font-size:12.5px;font-weight:700;color:var(--ink-soft);background:#fff;border:2px solid var(--beige);border-radius:999px;padding:5px 13px;text-decoration:none">日本語</a>'
      f'<a href="ranking-{metric}-en.html" style="font-size:12.5px;font-weight:700;color:var(--ink-soft);background:#fff;border:2px solid var(--beige);border-radius:999px;padding:5px 13px;text-decoration:none">English</a>'
      '<span style="font-size:12.5px;font-weight:800;color:#fff;background:var(--pink-deep);border:2px solid var(--pink-deep);border-radius:999px;padding:5px 13px">简体中文</span>'
      '</div>')

STYLE=re.search(r'<style>(.*?)</style>', open(os.path.join(ROOT,"ranking-loyalty-en.html"),encoding="utf-8").read(), re.DOTALL).group(1)

TEMPLATE="""<!DOCTYPE html>
<html lang="{htmllang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{sub}">
<meta property="og:type" content="website">
<meta property="og:locale" content="{locale}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{sub}">
<meta property="og:url" content="https://16lovetypedogs.com/ranking-{metric}-{lang}.html">
<meta property="og:image" content="https://16lovetypedogs.com/ogp.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="https://16lovetypedogs.com/ranking-{metric}-{lang}.html">
<link rel="alternate" hreflang="ja" href="https://16lovetypedogs.com/ranking-{metric}.html">
<link rel="alternate" hreflang="en" href="https://16lovetypedogs.com/ranking-{metric}-en.html">
<link rel="alternate" hreflang="zh-Hans" href="https://16lovetypedogs.com/ranking-{metric}-zh.html">
<link rel="alternate" hreflang="x-default" href="https://16lovetypedogs.com/ranking-{metric}-en.html">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c:wght@400;500;700;800&family=Baloo+2:wght@500;700;800&family=Zen+Maru+Gothic:wght@500;700&display=swap" rel="stylesheet">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9187493483642692" crossorigin="anonymous"></script>
<style>{style}</style>
</head><body>
<header>
  <div class="hinner">
    <a class="site-logo" href="/">{site}</a>
    <nav>
      <a href="/">{quiz}</a>
      <a href="{types_href}">{types}</a>
      <a href="{privacy_href}">{privacy}</a>
    </nav>
  </div>
</header><div class="wrap">
  {langbar}
  <div class="breadcrumb"><a href="/">{quiz}</a> › <a href="{types_href}">{types}</a> › {short}</div>
  <div class="hero"><h1 style="font-size:clamp(18px,4.5vw,24px);font-weight:800;color:var(--pink-deep);line-height:1.5">{title}</h1><p class="sub">{sub}</p></div>
  <div class="card"><p>{intro}</p><p style="font-size:12.5px;color:var(--ink-soft)">{reference}</p></div>
  <div class="card"><h2 style="font-size:17px;font-weight:800;color:var(--pink-deep);margin-bottom:12px;padding-bottom:8px;border-bottom:2px solid var(--beige)">{ranking}</h2>{items}</div>
  <div class="card" style="text-align:center"><p style="margin-bottom:12px;font-size:14.5px">🐾 16 Love-Type Dogs</p><a class="btn-back" href="/" style="background:var(--pink-deep);color:#fff;border-color:var(--pink-deep)">{cta}</a></div>
  <div class="card"><h2 style="font-size:17px;font-weight:800;color:var(--pink-deep);margin-bottom:10px;padding-bottom:8px;border-bottom:2px solid var(--beige)">{related_h}</h2>{related}</div>
</div>
<script type="application/ld+json">{ldjson}</script>
<footer>
  <div style="margin-bottom:8px"><a href="/">{quiz}</a> ｜ <a href="{types_href}">{types}</a> ｜ <a href="{privacy_href}">{privacy}</a></div>
  {disc}
</footer>
</body></html>
"""

def build(metric):
    M=META[metric]
    ldjson=json.dumps({"@context":"https://schema.org","@type":"Article","headline":M["title"],
        "description":M["sub"],"inLanguage":CHROME["htmllang"],
        "url":f"https://16lovetypedogs.com/ranking-{metric}-{LANG}.html",
        "publisher":{"@type":"Organization","name":"16 Love-Type Dogs","url":"https://16lovetypedogs.com"}},ensure_ascii=False)
    out=TEMPLATE.format(htmllang=CHROME["htmllang"],locale=CHROME["locale"],title=esc(M["title"]),sub=esc(M["sub"]),
        intro=esc(M["intro"]),metric=metric,lang=LANG,style=STYLE,site=CHROME["site"],quiz=CHROME["quiz"],
        types=CHROME["types"],types_href=CHROME["types_href"],privacy=CHROME["privacy"],privacy_href=CHROME["privacy_href"],
        langbar=langbar(metric),short=esc(REL_LABEL[metric]),reference=CHROME["reference"],ranking=CHROME["ranking"],
        items=rank_items(metric),cta=CHROME["cta"],related_h=CHROME["related"],related=related(metric),
        ldjson=ldjson,disc=CHROME["disc"])
    open(os.path.join(ROOT,f"ranking-{metric}-{LANG}.html"),"w",encoding="utf-8").write(out)

if __name__=="__main__":
    for m in ALL: build(m)
    print("generated 5 ZH ranking pages")
