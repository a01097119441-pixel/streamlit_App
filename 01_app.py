import streamlit as st
import random
import base64

st.set_page_config(
    page_title="🍀 오늘 뭐 먹지?",
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
    font-size:60px;
    font-weight:900;
    text-align:center;
    color:#FF1493;
    text-shadow:4px 4px #FFD700;
}

.subtitle{
    text-align:center;
    font-size:22px;
    color:#555;
    margin-bottom:30px;
}

.food-card{
    background:white;
    border-radius:30px;
    padding:30px;
    border:5px dashed hotpink;
    box-shadow:8px 8px 0 #FFD700;
    text-align:center;
    margin-top:25px;
}

.foodemoji{
    font-size:90px;
    animation: bounce 1.2s infinite;
}

.foodname{
    font-size:40px;
    font-weight:bold;
    color:#FF1493;
}

.category{
    font-size:22px;
    color:#666;
}

.fortune-card{
    background:#FFE4F2;
    border-radius:25px;
    border:4px solid hotpink;
    padding:20px;
    margin-top:25px;
    font-size:22px;
    text-align:center;
}

.stButton>button{
    width:100%;
    height:70px;
    font-size:30px;
    font-weight:bold;
    background:#FF1493;
    color:white;
    border:none;
    border-radius:18px;
}

.stButton>button:hover{
    background:#ff4fb4;
}

@keyframes bounce{
0%{transform:translateY(0);}
50%{transform:translateY(-10px);}
100%{transform:translateY(0);}
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# 음식 리스트
# -----------------------------

foods = [

# 한식
{
"emoji":"🍚",
"name":"비빔밥",
"category":"한식",
"fortune":"새로운 시작에 좋은 하루입니다."
},

{
"emoji":"🍲",
"name":"김치찌개",
"category":"한식",
"fortune":"따뜻한 위로가 필요한 날입니다."
},

{
"emoji":"🥘",
"name":"된장찌개",
"category":"한식",
"fortune":"안정적인 하루를 보낼 수 있습니다."
},

{
"emoji":"🍖",
"name":"삼겹살",
"category":"한식",
"fortune":"에너지가 넘치는 하루입니다."
},

{
"emoji":"🍗",
"name":"닭갈비",
"category":"한식",
"fortune":"친구와 함께하면 행운이 커집니다."
},

{
"emoji":"🍜",
"name":"칼국수",
"category":"한식",
"fortune":"마음이 편안해지는 하루입니다."
},

{
"emoji":"🍜",
"name":"냉면",
"category":"한식",
"fortune":"시원한 선택이 좋은 결과를 가져옵니다."
},

{
"emoji":"🍱",
"name":"제육볶음",
"category":"한식",
"fortune":"도전하면 좋은 결과가 있습니다."
},

{
"emoji":"🥟",
"name":"만둣국",
"category":"한식",
"fortune":"가족과 시간을 보내면 좋습니다."
},

{
"emoji":"🍛",
"name":"카레",
"category":"한식",
"fortune":"집중력이 높아지는 날입니다."
},

# 일식

{
"emoji":"🍣",
"name":"초밥",
"category":"일식",
"fortune":"금전운이 상승합니다."
},

{
"emoji":"🍜",
"name":"라멘",
"category":"일식",
"fortune":"새로운 인연이 생깁니다."
},

{
"emoji":"🍤",
"name":"텐동",
"category":"일식",
"fortune":"뜻밖의 행운이 찾아옵니다."
},

{
"emoji":"🍛",
"name":"가츠카레",
"category":"일식",
"fortune":"노력이 인정받습니다."
},

{
"emoji":"🍱",
"name":"규동",
"category":"일식",
"fortune":"소소한 행복이 있습니다."
},

{
"emoji":"🍢",
"name":"오뎅",
"category":"일식",
"fortune":"몸과 마음이 따뜻해집니다."
},

{
"emoji":"🥟",
"name":"교자",
"category":"일식",
"fortune":"좋은 소식이 들립니다."
},

{
"emoji":"🍳",
"name":"오므라이스",
"category":"일식",
"fortune":"웃을 일이 생깁니다."
},
# -----------------------------
# 양식
# -----------------------------

{
"emoji":"🍕",
"name":"페퍼로니 피자",
"category":"양식",
"fortune":"즐거운 만남이 기다립니다."
},

{
"emoji":"🍔",
"name":"치즈버거",
"category":"양식",
"fortune":"도전이 성공으로 이어집니다."
},

{
"emoji":"🍝",
"name":"까르보나라",
"category":"양식",
"fortune":"기분 좋은 일이 생깁니다."
},

{
"emoji":"🍝",
"name":"토마토 파스타",
"category":"양식",
"fortune":"활력이 넘치는 하루입니다."
},

{
"emoji":"🥩",
"name":"스테이크",
"category":"양식",
"fortune":"큰 기회를 잡을 수 있습니다."
},

{
"emoji":"🌭",
"name":"핫도그",
"category":"양식",
"fortune":"소소한 행운이 따릅니다."
},

{
"emoji":"🥪",
"name":"샌드위치",
"category":"양식",
"fortune":"가벼운 마음이 행운을 부릅니다."
},

{
"emoji":"🥗",
"name":"시저샐러드",
"category":"양식",
"fortune":"건강운이 좋아집니다."
},

# -----------------------------
# 중식
# -----------------------------

{
"emoji":"🥟",
"name":"짜장면",
"category":"중식",
"fortune":"행운이 찾아옵니다."
},

{
"emoji":"🌶",
"name":"짬뽕",
"category":"중식",
"fortune":"열정이 빛나는 하루입니다."
},

{
"emoji":"🍚",
"name":"볶음밥",
"category":"중식",
"fortune":"새로운 아이디어가 떠오릅니다."
},

{
"emoji":"🍖",
"name":"탕수육",
"category":"중식",
"fortune":"기쁜 소식을 듣게 됩니다."
},

{
"emoji":"🥟",
"name":"딤섬",
"category":"중식",
"fortune":"여유를 가지면 좋은 일이 생깁니다."
},

{
"emoji":"🍆",
"name":"마파두부",
"category":"중식",
"fortune":"과감한 선택이 행운을 부릅니다."
},

# -----------------------------
# 분식
# -----------------------------

{
"emoji":"🌶",
"name":"떡볶이",
"category":"분식",
"fortune":"스트레스가 풀립니다."
},

{
"emoji":"🍢",
"name":"순대",
"category":"분식",
"fortune":"좋은 사람을 만나게 됩니다."
},

{
"emoji":"🍢",
"name":"어묵",
"category":"분식",
"fortune":"따뜻한 하루를 보냅니다."
},

{
"emoji":"🍙",
"name":"김밥",
"category":"분식",
"fortune":"계획이 순조롭게 진행됩니다."
},

{
"emoji":"🍜",
"name":"라볶이",
"category":"분식",
"fortune":"행복한 일이 생깁니다."
},

{
"emoji":"🍟",
"name":"감자튀김",
"category":"분식",
"fortune":"작은 행운이 이어집니다."
},

# -----------------------------
# 멕시칸
# -----------------------------

{
"emoji":"🌮",
"name":"타코",
"category":"멕시칸",
"fortune":"예상 밖의 즐거움이 있습니다."
},

{
"emoji":"🌯",
"name":"부리또",
"category":"멕시칸",
"fortune":"새로운 경험이 기다립니다."
},

{
"emoji":"🧀",
"name":"나초",
"category":"멕시칸",
"fortune":"친구와 함께하면 더 좋습니다."
},

{
"emoji":"🥙",
"name":"케사디야",
"category":"멕시칸",
"fortune":"좋은 선택을 하게 됩니다."
},

# -----------------------------
# 디저트
# -----------------------------

{
"emoji":"🍰",
"name":"치즈케이크",
"category":"디저트",
"fortune":"달콤한 하루가 됩니다."
},

{
"emoji":"🧇",
"name":"와플",
"category":"디저트",
"fortune":"웃을 일이 생깁니다."
},

{
"emoji":"🍩",
"name":"도넛",
"category":"디저트",
"fortune":"행운이 한 바퀴 돌아옵니다."
},

{
"emoji":"🍨",
"name":"아이스크림",
"category":"디저트",
"fortune":"기분이 상쾌해집니다."
},

{
"emoji":"🧋",
"name":"버블티",
"category":"디저트",
"fortune":"새로운 친구를 만날 수 있습니다."
}

]
# -----------------------------
# 제목
# -----------------------------

st.markdown("""
<div class="bigtitle">
🍀 오늘 뭐 먹지? 🍀
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="subtitle">
운세가 오늘의 메뉴를 골라드립니다 ✨
</div>
""", unsafe_allow_html=True)

# -----------------------------
# 랜덤 데이터
# -----------------------------

lucky_colors = [
    "💛 노랑",
    "💙 파랑",
    "💚 초록",
    "❤️ 빨강",
    "🩷 핑크",
    "💜 보라",
    "🧡 주황",
    "🤍 하양"
]

quotes = [
    "오늘도 맛있는 하루가 될 거예요 🍀",
    "행운은 맛있는 음식과 함께 찾아옵니다 ✨",
    "배부르면 행복도 따라옵니다 😋",
    "오늘은 고민하지 말고 즐겨보세요 🌈",
    "맛있는 한 끼가 최고의 힐링입니다 💖",
    "오늘의 선택이 최고의 선택이 될 거예요 🎉",
    "행복은 가까운 식탁 위에 있습니다 🍽️",
    "좋은 음식은 좋은 기분을 만듭니다 🌸"
]

# -----------------------------
# 버튼
# -----------------------------

if st.button("🔮 오늘의 운세 뽑기"):

    result = random.choice(foods)

    lucky_color = random.choice(lucky_colors)

    quote = random.choice(quotes)

    st.markdown(f"""
    <div class="food-card">

        <div class="foodemoji">
            {result["emoji"]}
        </div>

        <div class="foodname">
            {result["name"]}
        </div>

        <br>

        <div class="category">
            📌 {result["category"]}
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="fortune-card">

    ✨ <b>오늘의 운세</b>

    <br><br>

    {result["fortune"]}

    <hr>

    🌈 <b>행운의 색</b>

    <br>

    {lucky_color}

    <hr>

    💬 {quote}

    </div>
    """, unsafe_allow_html=True)

    st.balloons()
    # -----------------------------
# 구분선
# -----------------------------

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<hr style="
border:0;
height:3px;
background:linear-gradient(to right,#FF1493,#FFD700,#00D4FF,#FF1493);
border-radius:10px;
">
""", unsafe_allow_html=True)

# -----------------------------
# 안내 문구
# -----------------------------

st.markdown("""
<div style="
text-align:center;
font-size:20px;
margin-top:15px;
color:#666;
">

🎲 버튼을 다시 누르면 새로운 메뉴와 운세가 나와요!

</div>
""", unsafe_allow_html=True)

# -----------------------------
# 푸터
# -----------------------------

st.markdown("""
<br><br>

<div style="
text-align:center;
padding:20px;
">

<h2 style="
color:#FF1493;
margin-bottom:10px;
">
🌈 Eat by Fortune 🌈
</h2>

<p style="
font-size:18px;
color:#666;
">
키치 감성 운세 맛집
</p>

<p style="
font-size:15px;
color:#999;
">
오늘의 식사도 행운과 함께 ✨
</p>

</div>
""", unsafe_allow_html=True)

# -----------------------------
# 사이드바
# -----------------------------

with st.sidebar:

    st.markdown("## 🍀 오늘 뭐 먹지?")

    st.markdown("""
이 앱은 랜덤으로 음식을 추천하고
오늘의 운세를 알려줍니다.

버튼을 눌러 오늘의 메뉴를 확인해보세요!
""")

    st.markdown("---")

    st.markdown("### 🎯 포함된 카테고리")

    st.markdown("""
- 🍚 한식
- 🍣 일식
- 🍕 양식
- 🥟 중식
- 🌮 멕시칸
- 🍢 분식
- 🍰 디저트
""")

    st.markdown("---")

    st.markdown("💖 Made with Streamlit")

# -----------------------------
# 끝
# -----------------------------
