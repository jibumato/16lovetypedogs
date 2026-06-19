#!/usr/bin/env python3
"""Generate the 5 Korean ranking pages (ranking-*-ko.html)."""
import re, os, json, html
ROOT=os.path.dirname(os.path.abspath(__file__))
src=open(os.path.join(ROOT,"index.html"),encoding="utf-8").read()
LOC=json.loads(re.search(r'\nconst LOC=(\{.*?\});\n',src,re.DOTALL).group(1))
KO=LOC["ko"]; LANG="ko"

STARS={
 'loyalty':{'INTJ':5,'INTP':4,'ENTJ':4,'ENTP':2,'INFJ':5,'INFP':5,'ENFJ':4,'ENFP':3,'ISTJ':5,'ISFJ':5,'ESTJ':4,'ESFJ':4,'ISTP':3,'ISFP':3,'ESTP':2,'ESFP':3},
 'devotion':{'INTJ':3,'INTP':2,'ENTJ':4,'ENTP':2,'INFJ':4,'INFP':4,'ENFJ':5,'ENFP':4,'ISTJ':3,'ISFJ':5,'ESTJ':4,'ESFJ':5,'ISTP':2,'ISFP':3,'ESTP':3,'ESFP':4},
 'marriage':{'INTJ':4,'INTP':2,'ENTJ':4,'ENTP':2,'INFJ':4,'INFP':3,'ENFJ':4,'ENFP':2,'ISTJ':5,'ISFJ':5,'ESTJ':5,'ESFJ':4,'ISTP':2,'ISFP':3,'ESTP':2,'ESFP':3},
 'jealousy':{'INTJ':4,'INTP':1,'ENTJ':3,'ENTP':2,'INFJ':3,'INFP':3,'ENFJ':3,'ENFP':4,'ISTJ':2,'ISFJ':3,'ESTJ':3,'ESFJ':5,'ISTP':2,'ISFP':2,'ESTP':3,'ESFP':5},
 'dokidoki':{'INTJ':2,'INTP':2,'ENTJ':3,'ENTP':5,'INFJ':2,'INFP':3,'ENFJ':3,'ENFP':5,'ISTJ':1,'ISFJ':1,'ESTJ':2,'ESFJ':3,'ISTP':3,'ISFP':3,'ESTP':5,'ESFP':5},
}
def stars(n): return "★"*n+"☆"*(5-n)

META={
 "loyalty":{"ja":"ranking-loyalty.html","title":"가장 일편단심인 MBTI 순위 TOP16｜바람 안 피우는 연애 유형은?【견종으로 풀이】",
   "sub":"한번 좋아하면 한 사람만. 바람과는 거리가 먼 '일편단심 강아지'는 누구?",
   "intro":"\"한번 사랑하면 그 사람이 전부.\" 얼마나 한결같은지는 성격 유형과 깊은 관련이 있습니다. 이 순위는 MBTI 16가지 유형을 견종에 빗대어, 연애에서의 일편단심 정도가 높은 순으로 정리했어요. 당신의 유형은 의외일지도?"},
 "marriage":{"ja":"ranking-marriage.html","title":"결혼에 가장 어울리는 MBTI 순위 TOP16｜누구와 결혼하면 행복할까?【견종으로 풀이】",
   "sub":"듬직하고 믿음직하며 따뜻한 — 결혼 생활에 어울리는 강아지는?",
   "intro":"\"연애에 좋은\" 것과 \"결혼에 좋은\" 것은 늘 같지 않습니다. 안정적인 가정을 꾸리는 데 얼마나 어울리는지는 성격 유형과 깊은 관련이 있어요. 이 순위는 MBTI 16가지 유형을 견종에 빗대어 결혼 적합도가 높은 순으로 정리했습니다."},
 "jealousy":{"ja":"ranking-jealousy.html","title":"가장 질투 많은 MBTI 순위 TOP16｜독점욕 강한 연애 유형은?【견종으로 풀이】",
   "sub":"살짝의 질투는 귀엽지만 — 누가 가장 세게 질투할까?",
   "intro":"질투가 난다는 건 그만큼 마음이 있다는 증거. 다만 얼마나 겉으로 드러나는지는 성격 유형과 깊은 관련이 있어요. 이 순위는 MBTI 16가지 유형을 견종에 빗대어 질투심이 강한 순으로 정리했습니다."},
 "devotion":{"ja":"ranking-devotion.html","title":"가장 헌신적인 MBTI 순위 TOP16｜정 깊은 연애 유형은?【견종으로 풀이】",
   "sub":"가득한 관심과 정성 — 사랑을 위해 가장 헌신하는 강아지는?",
   "intro":"좋아하는 사람을 위해 자꾸만 베풀게 되는 사람이 있죠. 연애에서 얼마나 헌신하는지는 성격 유형과 깊은 관련이 있어요. 이 순위는 MBTI 16가지 유형을 견종에 빗대어 헌신도가 높은 순으로 정리했습니다."},
 "dokidoki":{"ja":"ranking-dokidoki.html","title":"가장 설레게 하는 MBTI 순위 TOP16｜가장 짜릿한 연애 유형은?【견종으로 풀이】",
   "sub":"한순간도 지루하지 않은 — 계속 두근거리게 하는 강아지는?",
   "intro":"매일 가슴을 두근거리게 하는 사람이 있어요. 얼마나 설렘을 주는지는 성격 유형과 깊은 관련이 있습니다. 이 순위는 MBTI 16가지 유형을 견종에 빗대어 설렘도가 높은 순으로 정리했어요."},
}

TX={
 "loyalty":{
  "INTJ":"경계심 강한 치와와는 마음을 여는 데 오래 걸리는 만큼, 한번 '이 사람'이라 정하면 그 한결같음은 보증수표. 정해둔 사람 외에는 거의 한눈을 팔지 않아요.",
  "INFJ":"카발리에는 '운명의 단 한 사람'을 믿는 깊은 사랑형. 쉽게 좋아하지 않는 만큼, 선택한 상대에게는 자신의 전부를 바치듯 사랑합니다.",
  "INFP":"이상적인 사랑을 꿈꾸는 말티즈는 좋아하는 사람을 마음속 특등석에 오래도록 모셔두는 타입. 마음의 깊이와 지속력은 최상급이에요.",
  "ISTJ":"시바견은 연애계의 장인. 화려하지 않아도 한번 정한 상대를 무슨 일이 있어도 평생 소중히 하는, 고전적이고 흔들림 없는 일편단심의 소유자.",
  "ISFJ":"시츄는 좋아하는 사람 곁에 살며시 머무는 헌신형. 마음이 잘 변하지 않고 오랜 시간 같은 사람을 사랑합니다.",
  "INTP":"슈나우저는 연애에 담백해 보여도 빠지면 깊이 파고드는 탐구형. 스위치가 켜진 상대를 향한 관심은 오래갑니다.",
  "ENTJ":"코기는 '이 사람'이라 정하면 전력으로 지켜내는 리더형. 연애의 주도권은 쥐고 싶어 하지만 변심 걱정은 적은 타입.",
  "ENFJ":"골든은 사교적이고 인기 많지만 본命에 대한 충성심은 강한 편. 모두에게 다정해도 마음 한가운데는 오직 한 사람의 것.",
  "ESTJ":"보스턴테리어는 미래를 내다보며 성실하게 마주하는 견실파. 애매한 관계나 들뜬 연애를 좋아하지 않고 정한 사람만 바라봅니다.",
  "ESFJ":"래브라도는 애정이 넘치는 살뜰한 타입. 외로움을 타는 면은 있어도 사랑하는 사람을 향한 마음은 곧고 진실합니다.",
  "ENFP":"푸들은 변덕스러워 보여도 본바탕은 일편단심. 마음을 연 상대에게는 활기찬 애정을 곧게 쏟아붓습니다.",
  "ISTP":"닥스훈트는 쿨하고 집착이 옅은 편. 다만 신뢰한 상대에 대한 조용한 충성심은 말로 안 할 뿐 분명히 존재해요.",
  "ISFP":"프렌치불독은 마이페이스인 자유인이지만, 편안한 상대와는 오래 잔잔하게 이어지는 타입. 격렬하진 않아도 안정적이에요.",
  "ESFP":"포메는 연애의 주인공이고 싶은 사랑받고 싶은 타입. 사랑받는 실감이 있을 땐 일편단심이지만 방치되면 불안정해집니다.",
  "ENTP":"잭러셀은 연애의 사냥꾼 기질. 쫓을 때가 가장 뜨겁고, 안정기에 접어들면 새로운 자극을 찾고 싶어지기도.",
  "ESTP":"비글은 자극을 좇는 행동파. 마음은 솔직하고 직진이지만 지루한 관계에서는 열기가 식기 쉬운 경향도.",
 },
 "devotion":{
  "ENFJ":"헌신도 1위는 골든리트리버. 상대의 행복이 곧 내 행복이라 기념일도 사소한 배려도 완벽. 다만 너무 헌신해 자신을 뒷전에 두기 쉬우니 사랑을 돌려주세요.",
  "ISFJ":"시츄는 '티 안 나게' 헌신하는 프로. 부탁하기 전에 알아채고 움직여 주는, 가려운 곳을 긁어 주는 헌신파.",
  "ESFJ":"래브라도는 애정 표현이 직진이고 아낌없습니다. 부지런한 연락, 손수 만든 요리, 깜짝 이벤트 — 사랑받는 실감을 가득 줘요.",
  "ENTJ":"코기는 행동으로 헌신하는 타입: 지키고, 받쳐 주고, 이끌어 줍니다. 곤란할 때 가장 든든한 존재예요.",
  "INFJ":"카발리에는 말로 안 한 마음까지 헤아려 주는 섬세한 헌신형. 마음을 돌보는 솜씨가 으뜸입니다.",
  "INFP":"말티즈는 좋아하는 사람을 위해서라면 자연스레 힘내는 순수한 헌신가. 보답을 바라지 않는 사랑법이 매력.",
  "ENFP":"푸들은 '함께 즐기기'로 사랑을 쏟는 타입. 깜짝 이벤트와 행사 기획력은 단연 최고예요.",
  "ESTJ":"보스턴테리어는 안정과 계획으로 헌신하는 견실파. 화려하진 않아도 생활을 떠받치는 힘은 진짜입니다.",
  "ESFP":"포메는 사랑받는 것도 좋아하지만 좋아하는 사람을 기쁘게 하는 것도 무척 좋아해요. 리액션까지 곁들여 즐겁게 헌신합니다.",
  "INTJ":"치와와는 본命 한정 헌신형. 밖에선 안 보이는 응석과 애정을 둘만 있을 때만 발동합니다.",
  "ISTJ":"시바견은 말주변이 없어도 행동으로 보여줍니다. 약속을 지키고 시간을 지키는 그 쌓임이 곧 애정 표현이에요.",
  "ISFP":"프렌치불독은 곁에 있어 주는 것만으로 당신을 치유합니다. 무언가를 '해 주는' 것보다 '함께 있어 주는' 헌신.",
  "ESTP":"비글은 즐거운 경험을 선사하는 엔터테이너형. 우울한 날 당신을 밖으로 데리고 나가는 건 바로 이 유형.",
  "INTP":"슈나우저는 서툴지만 당신의 관심사를 누구보다 잘 기억하는 관찰형. 가끔 던지는 한마디가 깊이 박힙니다.",
  "ENTP":"잭러셀은 헌신보다 즐겁게 해 주는 쪽. 지루하지 않은 매일이라는, 또 다른 형태의 선물을 줍니다.",
  "ISTP":"닥스훈트는 평소엔 무심해도 정말 곤란할 때 말없이 나서 주는 '결정적 순간'형 헌신이에요.",
 },
 "marriage":{
  "ISTJ":"시바견은 약속을 지키고 차곡차곡 신뢰를 쌓는 견실파. 기념일을 잊지 않고 가계도 생활도 계획적. '결혼해서 안심되는 사람'의 대표격입니다.",
  "ISFJ":"시츄는 결혼 적합도의 정점. 티 안 나는 배려, 헌신, 안정감 삼박자를 갖춰 매일의 삶을 따뜻하게 받쳐 주는 파트너가 돼요.",
  "ESTJ":"보스턴테리어는 가정이라는 '팀'을 빈틈없이 운영할 수 있는 타입. 책임감이 강하고 가족을 지키는 기둥 기질입니다.",
  "INTJ":"치와와는 결혼을 '인생 전략'으로 진지하게 고민하는 타입. 결정까지는 신중하지만 정한 뒤의 안정감은 발군이에요.",
  "ENTJ":"코기는 가정의 미래 설계까지 든든히 이끄는 존재. 맞벌이라도 한쪽에 떠넘기지 않는 계획성이 매력입니다.",
  "INFJ":"카발리에는 깊은 정신적 유대를 쌓는 평생의 파트너. 화려하진 않아도 마음이 통하는 가정을 만듭니다.",
  "ENFJ":"골든은 가족의 행복이 곧 내 행복인 헌신형. 따뜻한 가정의 중심, 태양 같은 존재가 돼요.",
  "ESFJ":"래브라도는 가족 행사를 소중히 하는 애정 풍부한 타입. 떠들썩하고 따뜻한 가정을 만듭니다.",
  "INFP":"말티즈는 가정에 이상과 다정함을 들이는 로맨티스트. 안심되는 상대와는 깊은 유대의 가정을 꾸릴 수 있어요.",
  "ISFP":"프렌치불독은 다툼 없는 평온한 가정을 좋아하는 평화주의자. 느긋한 공기의 편안한 집이 됩니다.",
  "ESFP":"포메는 가정을 밝히는 분위기 메이커. 매일을 즐겁게 해 주지만 집안일 계획성은 파트너의 보조가 있으면 좋아요.",
  "INTP":"슈나우저는 생활감보다 지적인 세계를 중시하는 타입. 집안일 분담을 시스템화할 수 있는 상대와 함께라면 쾌적합니다.",
  "ENTP":"잭러셀은 자유와 자극을 사랑하는 모험가. 틀에 박힌 결혼상보다 둘만의 형태를 만들 수 있는 상대가 필요해요.",
  "ENFP":"푸들은 결혼해도 연인 기분을 잃고 싶지 않은 타입. 권태기 대책을 함께 즐길 수 있는 상대와 오래갑니다.",
  "ISTP":"닥스훈트는 간섭하지 않는 독립적인 부부 관계를 선호하는 타입. 끈적이지 않는 어른스러운 결혼 생활이 잘 맞아요.",
  "ESTP":"비글은 활동적인 가족의 놀이 담당. 추진력으로 가정에 이벤트를 만들지만 차분히 자리 잡는 건 아직 진행 중.",
 },
 "jealousy":{
  "ESFJ":"래브라도는 '받은 만큼 사랑받고 싶은' 타입. 돌아오는 애정이 옅다고 느끼면 질투와 외로움이 고개를 듭니다.",
  "ESFP":"당당한 1위는 포메. 관심받고 사랑받고 싶어 해서 연인의 관심이 다른 데로 향하면 온몸으로 안절부절. 알기 쉬운 질투는 귀여움이기도 해요.",
  "INTJ":"의외의 상위권은 치와와. 겉으론 쿨한데 속에선 독점욕이 슬금슬금 자랍니다. 입 밖에 안 내는 만큼 쌓아두기 쉬운 타입.",
  "ENFP":"푸들은 떠들썩하고 자유로워 보여도 사실은 외로움을 타요. 연인의 연락이 줄면 불안해져 질투를 부리기 쉽습니다.",
  "ENTJ":"코기의 독점욕엔 지기 싫어하는 마음이 섞여 있어요. 라이벌이 나타나면 질투보다 '투지'로 맞섭니다.",
  "INFJ":"카발리에는 '나만 봐 줬으면' 하는 깊은 사랑형. 평소엔 참지만 한계를 넘으면 조용히 흘러넘칩니다.",
  "INFP":"말티즈는 마음이 깊은 만큼 불안도 잘 자라는 타입. 말로 못 하고 혼자 몰래 상처받기도 해요.",
  "ENFJ":"골든은 질투보다 '상대의 행복'을 우선해 버리는 무사(無私)의 사랑. 오히려 너무 참는 게 걱정이에요.",
  "ISFJ":"시츄는 질투해도 겉으로 안 드러내고 살며시 참는 기특한 타입. 알아채 줄 수 있느냐가 관건입니다.",
  "ESTJ":"보스턴은 파트너의 행동이 '앞뒤가 안 맞는다' 느낄 때 언짢아지는 타입. 질투라기보다 질서의 문제예요.",
  "ESTP":"비글은 담아두지 않는 깔끔한 기질. 한순간 욱해도 즐거운 일이 생기면 금세 잊어버립니다.",
  "ENTP":"잭러셀은 쫓는 걸 즐기는 편이라 질투도 게임 감각. 라이벌의 존재가 오히려 연료가 되기도 해요.",
  "ISTJ":"시바견은 신뢰를 전제로 사귀는 강직파. 의심 자체를 어려워해 질투보다 성실함으로 관계를 지킵니다.",
  "ISTP":"닥스훈트는 집착이 옅은 쿨함의 대표. 속박도 질투도 좋아하지 않고 자유와 신뢰의 관계를 바랍니다.",
  "ISFP":"프렌치불독은 온화한 평화주의자. 웬만한 건 '뭐 어때'로 넘길 수 있는, 질투가 적은 타입이에요.",
  "INTP":"슈나우저는 질투를 '비합리적'이라 느끼는 이성파. 신경 안 쓰는 게 아니라 분석해서 소화해 버립니다.",
 },
 "dokidoki":{
  "ENTP":"설렘도 1위는 잭러셀테리어. 재치 있는 대화, 예측 불가한 행동력, 절묘한 밀당. '지루함'이라는 단어가 사전에 없는 연애를 할 수 있어요.",
  "ENFP":"푸들은 호기심과 열정 덩어리. 새로운 놀이, 새로운 장소, 풍부한 감정 리액션으로 설렘이 계속됩니다.",
  "ESTP":"비글은 생각나면 바로 실행하는 스릴 메이커. '지금 바다 가자'가 진짜 시작되는, 생생한 현장감의 연애예요.",
  "ESFP":"포메는 매일을 주인공급으로 화려하게 만드는 엔터테이너. 함께 있는 것만으로 이벤트 같은 설렘이 가득.",
  "ENTJ":"코기는 강하게 이끌어 주는 설렘. 빠른 결단과 든든함에 불시에 가슴이 두근거립니다.",
  "INFP":"말티즈는 로맨틱한 세계관으로 설레게 하는 타입. 편지나 기념일 연출로 마음에 남는 순간을 만들어요.",
  "ENFJ":"골든은 왕도의 설렘 공급형. 에스코트에 능해 소중히 여겨지는 실감이 두근거림으로 바뀝니다.",
  "ESFJ":"래브라도는 직진 애정 표현으로 가슴을 두근하게 하는 타입. 아낌없이 '좋아해'를 말하는 솔직함이 무기.",
  "ISTP":"닥스훈트는 평소엔 쿨한데, 결정적 순간의 든든함으로 사로잡는 지효성 설렘이에요.",
  "ISFP":"프렌치불독은 잔잔함 속 문득 드러나는 진짜 모습에 설레는 타입. 서서히 효과가 옵니다.",
  "INTJ":"치와와는 쿨→다정의 반전이 매력인 갭 담당. 가끔 보이는 애교에 심장을 저격당해요.",
  "INTP":"슈나우저의 매력은 아무도 못 알아챈 시각을 주는 지적인 번뜩임. 똑똑한 사람을 좋아하는 이에게 제대로 꽂힙니다.",
  "INFJ":"카발리에는 깊은 대화로 마음의 거리가 좁혀지는 순간에 설레게 하는 정신적 두근거림형.",
  "ESTJ":"보스턴은 안정감이 매력인 만큼 설렘은 잔잔한 편. 대신 배신당할 걱정 없는 연애를 할 수 있어요.",
  "ISTJ":"시바견은 자극보다 신뢰의 사람. 설렘은 적어도 오래가는 안심이라는 최강의 토대를 줍니다.",
  "ISFJ":"시츄의 설렘은 '안심'과 한 세트. 문득 건네는 다정함에 마음이 뭉클 움직여요.",
 },
}

CHROME={"htmllang":"ko","locale":"ko_KR","suffix":"｜16 연애견 진단","site":"🐾 16 연애견 진단",
  "quiz":"진단하기","types":"유형 목록","privacy":"개인정보처리방침","cta":"🐶 진단하기","ranking":"순위",
  "related":"관련 글","reference":"참고용입니다. 「16 연애견 진단」의 연애 스탯 기반, 오락용입니다.",
  "types_href":"/types-ko.html","privacy_href":"/privacy.html","profile":"전체 프로필 보기",
  "disc":"※순위와 진단 결과는 오락용이며 심리학적·의학적 진단이 아닙니다.<br>※본 사이트는 제휴 링크(Amazon Associates)와 Google AdSense를 사용합니다.<br>© 2025 16 Love-Type Dogs / Mymatrix"}
REL_LABEL={"loyalty":"가장 일편단심인 MBTI 순위 TOP16","marriage":"결혼에 어울리는 MBTI 순위 TOP16",
  "jealousy":"가장 질투 많은 MBTI 순위 TOP16","devotion":"가장 헌신적인 MBTI 순위 TOP16","dokidoki":"가장 설레게 하는 MBTI 순위 TOP16"}
ALL=["loyalty","marriage","jealousy","devotion","dokidoki"]
SELF_LABEL="한국어"; OTHER_LANGS=[("ja","日本語","ranking-{m}.html"),("en","English","ranking-{m}-en.html"),("zh","简体中文","ranking-{m}-zh.html")]

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
        breed=esc(KO[code]["breed"]); name=esc(KO[code]["name"]); c=code.lower()
        blocks+=(f'<div class="rankitem">\n  <div class="rk">{marker}<img loading="lazy" decoding="async" src="/{c}.webp" alt="{breed}" style="width:54px;height:auto;border-radius:12px;margin-top:4px" onerror="this.style.display=\'none\'"></div>\n'
          f'  <div class="rbody">\n    <div class="nm">#{rank} {breed}（{code}）</div>\n    <div class="bd">{name}</div>\n'
          f'    <div class="st" style="color:#c79a3f;font-size:14px;letter-spacing:1.5px">{stars(STARS[metric][code])}</div>\n'
          f'    <p class="tx" style="font-size:13.5px;line-height:1.8;margin-top:5px">{esc(TX[metric][code])}</p>\n'
          f'    <a href="/type-{c}-{LANG}.html" style="font-size:12px;font-weight:700">→ {CHROME["profile"]} {breed}</a>\n  </div>\n</div>')
    return blocks

def related(metric):
    out=""
    for m in ALL:
        if m==metric: continue
        out+=(f'<a href="/ranking-{m}-{LANG}.html" style="display:block;background:var(--bg);border:1.5px solid var(--beige);border-radius:12px;padding:10px 14px;font-size:13px;font-weight:700;text-decoration:none">{REL_LABEL[m]}</a>')
    out+=(f'<a href="{CHROME["types_href"]}" style="display:block;background:var(--bg);border:1.5px solid var(--beige);border-radius:12px;padding:10px 14px;font-size:13px;font-weight:700;text-decoration:none">{CHROME["types"]}</a>')
    return out

def langbar(metric):
    parts=[]
    for lg,label,patt in OTHER_LANGS:
        parts.append(f'<a href="{patt.format(m=metric)}" style="font-size:12.5px;font-weight:700;color:var(--ink-soft);background:#fff;border:2px solid var(--beige);border-radius:999px;padding:5px 13px;text-decoration:none">{label}</a>')
    parts.append(f'<span style="font-size:12.5px;font-weight:800;color:#fff;background:var(--pink-deep);border:2px solid var(--pink-deep);border-radius:999px;padding:5px 13px">{SELF_LABEL}</span>')
    return '<div class="langbar" style="display:flex;justify-content:center;gap:6px;padding:12px 0;flex-wrap:wrap">'+"".join(parts)+'</div>'

STYLE=re.search(r'<style>(.*?)</style>', open(os.path.join(ROOT,"ranking-loyalty-en.html"),encoding="utf-8").read(), re.DOTALL).group(1)
HREF=('<link rel="alternate" hreflang="ja" href="https://16lovetypedogs.com/ranking-{metric}.html">\n'
 '<link rel="alternate" hreflang="en" href="https://16lovetypedogs.com/ranking-{metric}-en.html">\n'
 '<link rel="alternate" hreflang="ko" href="https://16lovetypedogs.com/ranking-{metric}-ko.html">\n'
 '<link rel="alternate" hreflang="zh-Hans" href="https://16lovetypedogs.com/ranking-{metric}-zh.html">\n'
 '<link rel="alternate" hreflang="x-default" href="https://16lovetypedogs.com/ranking-{metric}-en.html">')

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
{href}
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
    ldjson=json.dumps({"@context":"https://schema.org","@type":"Article","headline":M["title"],"description":M["sub"],
        "inLanguage":CHROME["htmllang"],"url":f"https://16lovetypedogs.com/ranking-{metric}-{LANG}.html",
        "publisher":{"@type":"Organization","name":"16 Love-Type Dogs","url":"https://16lovetypedogs.com"}},ensure_ascii=False)
    out=TEMPLATE.format(htmllang=CHROME["htmllang"],locale=CHROME["locale"],title=esc(M["title"]),sub=esc(M["sub"]),
        intro=esc(M["intro"]),metric=metric,lang=LANG,href=HREF.format(metric=metric),style=STYLE,site=CHROME["site"],
        quiz=CHROME["quiz"],types=CHROME["types"],types_href=CHROME["types_href"],privacy=CHROME["privacy"],
        privacy_href=CHROME["privacy_href"],langbar=langbar(metric),short=esc(REL_LABEL[metric]),reference=CHROME["reference"],
        ranking=CHROME["ranking"],items=rank_items(metric),cta=CHROME["cta"],related_h=CHROME["related"],
        related=related(metric),ldjson=ldjson,disc=CHROME["disc"])
    open(os.path.join(ROOT,f"ranking-{metric}-{LANG}.html"),"w",encoding="utf-8").write(out)

if __name__=="__main__":
    for m in ALL: build(m)
    print("generated 5 KO ranking pages")
