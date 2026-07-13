import streamlit as st
import random
import base64

st.set_page_config(
    page_title="오늘 뭐 먹지?",
    page_icon="🍀",
    layout="centered"
)

# -----------------------------
# CSS
# -----------------------------
st.markdown("""
<style>

body{
background:#FFF7E8;
}

.main{
padding-top:20px;
}

.bigtitle{
font-size:58px;
font-weight:900;
text-align:center;
color:#FF1493;
text-shadow:4px 4px #FFD700;
margin-bottom:10px;
}

.subtitle{
text-align:center;
font-size:22px;
color:#444;
margin-bottom:40px;
}

.food-card{
background:white;
padding:25px;
border-radius:25px;
border:5px dashed hotpink;
box-shadow:8px 8px 0px #FFD700;
margin-top:20px;
text-align:center;
}

.fortune-card{
background:#FFE4F2;
padding:20px;
border-radius:20px;
border:4px solid hotpink;
margin-top:25px;
font-size:22px;
}

.stButton>button{
width:100%;
background:#FF1493;
color:white;
font-size:28px;
font-weight:bold;
border-radius:18px;
height:70px;
border:none;
}

.stButton>button:hover{
background:#ff4fb4;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# SVG 일러스트
# -----------------------------

def bowl(color, food):
    return f"""
    <svg width="260" height="220" xmlns="http://www.w3.org/2000/svg">

    <ellipse cx="130" cy="160" rx="80" ry="25" fill="#ff6b81"/>

    <path d="M60 80
             Q130 210 200 80"
             fill="{color}"
             stroke="#333"
             stroke-width="5"/>

    <circle cx="100" cy="90" r="12" fill="#FFD93D"/>
    <circle cx="130" cy="75" r="12" fill="#6BCB77"/>
    <circle cx="160" cy="92" r="12" fill="#4D96FF"/>

    <text x="130" y="195"
    text-anchor="middle"
    font-size="22"
    font-weight="bold">
    {food}
    </text>

    </svg>
    """

foods = [
    # 🍚 한식
    {"name":"🍚 비빔밥","category":"한식","fortune":"새로운 시작에 좋은 하루입니다."},
    {"name":"🍲 김치찌개","category":"한식","fortune":"따뜻한 위로가 필요한 날입니다."},
    {"name":"🥘 된장찌개","category":"한식","fortune":"안정적인 하루를 보낼 수 있습니다."},
    {"name":"🍖 삼겹살","category":"한식","fortune":"에너지가 넘치는 하루입니다."},
    {"name":"🍗 닭갈비","category":"한식","fortune":"친구와 함께하면 행운이 커집니다."},
    {"name":"🍜 칼국수","category":"한식","fortune":"마음이 편안해지는 하루입니다."},
    {"name":"🍜 냉면","category":"한식","fortune":"시원한 선택이 좋은 결과를 가져옵니다."},
    {"name":"🍱 제육볶음","category":"한식","fortune":"도전하면 좋은 결과가 있습니다."},
    {"name":"🥟 만둣국","category":"한식","fortune":"가족과 시간을 보내면 좋습니다."},
    {"name":"🍛 카레","category":"한식","fortune":"집중력이 높아지는 날입니다."},

    # 🍣 일식
    {"name":"🍣 초밥","category":"일식","fortune":"금전운이 상승합니다."},
    {"name":"🍜 라멘","category":"일식","fortune":"새로운 인연이 생깁니다."},
    {"name":"🍤 텐동","category":"일식","fortune":"뜻밖의 행운이 찾아옵니다."},
    {"name":"🍛 가츠카레","category":"일식","fortune":"노력이 인정받습니다."},
    {"name":"🍱 규동","category":"일식","fortune":"소소한 행복이 있습니다."},
    {"name":"🍢 오뎅","category":"일식","fortune":"몸과 마음이 따뜻해집니다."},
    {"name":"🥟 교자","category":"일식","fortune":"좋은 소식이 들립니다."},
    {"name":"🍛 오므라이스","category":"일식","fortune":"웃을 일이 생깁니다."},

    # 🍕 양식
    {"name":"🍕 페퍼로니 피자","category":"양식","fortune":"즐거운 만남이 기다립니다."},
    {"name":"🍔 치즈버거","category":"양식","fortune":"도전이 성공으로 이어집니다."},
    {"name":"🍝 까르보나라","category":"양식","fortune":"기분 좋은 일이 생깁니다."},
    {"name":"🍝 토마토 파스타","category":"양식","fortune":"활력이 넘치는 하루입니다."},
    {"name":"🥩 스테이크","category":"양식","fortune":"큰 기회를 잡을 수 있습니다."},
    {"name":"🌭 핫도그","category":"양식","fortune":"소소한 행운이 따릅니다."},
    {"name":"🥪 샌드위치","category":"양식","fortune":"가벼운 마음이 행운을 부릅니다."},
    {"name":"🥗 시저샐러드","category":"양식","fortune":"건강운이 좋아집니다."},

    # 🌮 멕시칸
    {"name":"🌮 타코","category":"멕시칸","fortune":"예상 밖의 즐거움이 있습니다."},
    {"name":"🌯 부리또","category":"멕시칸","fortune":"새로운 경험이 기다립니다."},
    {"name":"🧀 나초","category":"멕시칸","fortune":"친구와 함께하면 더 좋습니다."},
    {"name":"🥙 케사디야","category":"멕시칸","fortune":"좋은 선택을 하게 됩니다."},

    # 🥡 중식
    {"name":"🥟 짜장면","category":"중식","fortune":"행운이 찾아옵니다."},
    {"name":"🌶 짬뽕","category":"중식","fortune":"열정이 빛나는 하루입니다."},
    {"name":"🍚 볶음밥","category":"중식","fortune":"새로운 아이디어가 떠오릅니다."},
    {"name":"🍖 탕수육","category":"중식","fortune":"기쁜 소식을 듣게 됩니다."},
    {"name":"🥟 딤섬","category":"중식","fortune":"여유를 가지면 좋은 일이 생깁니다."},
    {"name":"🍆 마파두부","category":"중식","fortune":"과감한 선택이 행운을 부릅니다."},

    # 🥤 분식
    {"name":"🌶 떡볶이","category":"분식","fortune":"스트레스가 풀립니다."},
    {"name":"🍢 순대","category":"분식","fortune":"좋은 사람을 만나게 됩니다."},
    {"name":"🍢 어묵","category":"분식","fortune":"따뜻한 하루를 보냅니다."},
    {"name":"🍙 김밥","category":"분식","fortune":"계획이 순조롭게 진행됩니다."},
    {"name":"🍜 라볶이","category":"분식","fortune":"행복한 일이 생깁니다."},
    {"name":"🍟 감자튀김","category":"분식","fortune":"작은 행운이 이어집니다."},

    # 🍰 디저트
    {"name":"🍰 치즈케이크","category":"디저트","fortune":"달콤한 하루가 됩니다."},
    {"name":"🧇 와플","category":"디저트","fortune":"웃을 일이 생깁니다."},
    {"name":"🍩 도넛","category":"디저트","fortune":"행운이 한 바퀴 돌아옵니다."},
    {"name":"🍨 아이스크림","category":"디저트","fortune":"기분이 상쾌해집니다."},
    {"name":"🧋 버블티","category":"디저트","fortune":"새로운 친구를 만날 수 있습니다."},
]

# -----------------------------
# 제목
# -----------------------------

st.markdown('<div class="bigtitle">🍀 오늘 뭐 먹지? 🍀</div>',
unsafe_allow_html=True)

st.markdown(
'<div class="subtitle">운세가 오늘의 메뉴를 골라드립니다 ✨</div>',
unsafe_allow_html=True)

# -----------------------------
# 버튼
# -----------------------------

if st.button("🔮 오늘의 운세 뽑기"):

    result = random.choice(foods)

    svg = bowl(result["color"], result["name"])

    b64 = base64.b64encode(svg.encode()).decode()

    st.markdown(f"""
    <div class="food-card">

    <img src="data:image/svg+xml;base64,{b64}" width="260">

    <h1>{result["name"]}</h1>

    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="fortune-card">

    ✨ <b>오늘의 운세</b><br><br>

    {result["fortune"]}

    </div>
    """, unsafe_allow_html=True)

    lucky = random.choice([
        "💛 행운의 색 : 노랑",
        "💙 행운의 색 : 파랑",
        "💚 행운의 색 : 초록",
        "🩷 행운의 색 : 핑크",
        "❤️ 행운의 색 : 빨강"
    ])

    st.success(lucky)

    st.balloons()

st.markdown(
"""
<br><br>
<center>
<h4>🌈 Eat by Fortune 🌈</h4>
<p>키치 감성 운세 맛집</p>
</center>
""",
unsafe_allow_html=True
)
