import streamlit as st

st.set_page_config(page_title="MoodMovie", page_icon="🎬")

movies = {
    "😊 행복": {
        "title": "인사이드 아웃",
        "genre": "애니메이션",
        "story": "기쁨, 슬픔 등 감정들이 펼치는 따뜻한 이야기.",
        "color": "#FFE066"
    },
    "😢 슬픔": {
        "title": "코코",
        "genre": "애니메이션",
        "story": "가족의 소중함과 추억을 그린 감동 영화.",
        "color": "#74C0FC"
    },
    "😍 설렘": {
        "title": "라라랜드",
        "genre": "로맨스",
        "story": "꿈과 사랑 사이에서 고민하는 두 사람의 이야기.",
        "color": "#FFB3C6"
    },
    "😎 액션": {
        "title": "탑건: 매버릭",
        "genre": "액션",
        "story": "최고의 파일럿이 펼치는 짜릿한 비행 액션.",
        "color": "#FF922B"
    },
    "😂 웃고 싶다": {
        "title": "극한직업",
        "genre": "코미디",
        "story": "형사들이 치킨집을 운영하며 벌어지는 코미디.",
        "color": "#69DB7C"
    },
    "😱 무섭다": {
        "title": "곤지암",
        "genre": "공포",
        "story": "폐병원을 탐험하며 벌어지는 공포 이야기.",
        "color": "#845EF7"
    }
}

mood = st.selectbox("😊 오늘의 기분은?", list(movies.keys()))

color = movies[mood]["color"]

st.markdown(f"""
<style>

.stApp {{
    background: linear-gradient(135deg, {color}, #ffffff);
}}

.title {{
    text-align:center;
    font-size:50px;
    font-weight:bold;
    color:#222;
}}

.card {{
    background:white;
    padding:30px;
    border-radius:25px;
    box-shadow:0px 8px 20px rgba(0,0,0,0.2);
    text-align:center;
}}

.movie {{
    font-size:35px;
    font-weight:bold;
    color:#333;
}}

.genre {{
    color:#666;
    font-size:20px;
}}

.story {{
    font-size:18px;
    line-height:1.8;
}}

</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🎬 MoodMovie 🍿</div>", unsafe_allow_html=True)

st.write("### 오늘 기분에 맞는 영화를 추천해드립니다!")

if st.button("🎲 영화 추천"):
    movie = movies[mood]

    st.markdown(f"""
    <div class="card">

    <div style="font-size:80px;">🎥</div>

    <div class="movie">
    {movie['title']}
    </div>

    <div class="genre">
    🎭 {movie['genre']}
    </div>

    <br>

    <div class="story">
    {movie['story']}
    </div>

    </div>
    """, unsafe_allow_html=True)

    st.balloons()
