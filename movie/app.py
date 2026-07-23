import streamlit as st

st.set_page_config(
    page_title="MoodMovie",
    page_icon="🎬",
    layout="centered"
)

movies = {
    "😊 행복": {
        "title": "인사이드 아웃",
        "genre": "애니메이션",
        "story": "라일리의 머릿속에는 기쁨, 슬픔, 버럭, 까칠, 소심이라는 다섯 감정이 살고 있습니다. 새로운 환경에서 여러 감정을 겪으며 진정한 행복과 성장의 의미를 깨닫는 따뜻한 감동 애니메이션입니다.",
        "color": "#FFE066",
        "poster": "0BiHlYxIl2KJ0KvR3PRDXvBrZ497r7sVbGbsFnX8NzcBiNqI_SERAonKt1DrX4YplofclKEk4d1Mg_KkBBqOa45nA5sFJH6-9XkaNvfimin6P5UfiuBtaOwaULUI1xHP3ld_j-7VCANkHlaSAQkhxQ"
    },

    "😢 슬픔": {
        "title": "코코",
        "genre": "애니메이션",
        "story": "음악을 사랑하는 소년 미구엘이 죽은 자들의 세상으로 떠나며 가족의 사랑과 추억의 소중함을 깨닫는 감동적인 이야기입니다.",
        "color": "#74C0FC",
        "poster": "8290_8563_418"
    },

    "😍 설렘": {
        "title": "라라랜드",
        "genre": "로맨스",
        "story": "배우를 꿈꾸는 미아와 재즈 피아니스트 세바스찬이 꿈과 사랑 사이에서 고민하며 성장하는 아름다운 뮤지컬 영화입니다.",
        "color": "#FFB3C6",
        "poster": "MHgGkv3aInGRnLq5bnY7tO834TratDtR-h3l2Ci05sCci6KWeLRuo1qB1YTjMHq3-nVv12wXCwH_D409fVFHfm-TMANWg4OOdK_EJgJX4eAma8CDI7rqgyC6MHzdMRvacmUVapz9occV4-uKm0jAAA"
    },

    "😎 액션": {
        "title": "탑건: 매버릭",
        "genre": "액션",
        "story": "전설적인 파일럿 매버릭이 젊은 조종사들과 함께 위험한 임무를 수행하며 최고의 비행 액션을 선보입니다.",
        "color": "#FF922B",
        "poster": "다운로드"
    },

    "😂 웃고 싶다": {
        "title": "극한직업",
        "genre": "코미디",
        "story": "범인을 잡기 위해 치킨집을 운영하게 된 형사들이 뜻밖의 대박을 맞으며 벌어지는 유쾌한 코미디 영화입니다.",
        "color": "#69DB7C",
        "poster": "다운로드 (1)"
    },

    "😱 무섭다": {
        "title": "곤지암",
        "genre": "공포",
        "story": "유명한 폐병원 곤지암을 실시간 방송으로 탐험하던 사람들이 설명할 수 없는 공포를 마주하게 되는 한국 공포 영화입니다.",
        "color": "#845EF7",
        "poster": "132246172.1"
    }
}

mood = st.selectbox(
    "😊 오늘의 기분을 선택하세요",
    list(movies.keys())
)

movie = movies[mood]

color = movie["color"]

st.markdown(f"""
<style>

.stApp {{
    background: linear-gradient(135deg, {color}, white);
}}

.title {{
    text-align:center;
    font-size:50px;
    font-weight:bold;
    color:#222;
}}

.subtitle {{
    text-align:center;
    font-size:20px;
    color:#555;
    margin-bottom:30px;
}}

.card {{
    background:white;
    padding:30px;
    border-radius:25px;
    box-shadow:0 8px 20px rgba(0,0,0,0.2);
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

st.markdown(
    "<div class='title'>🎬 MoodMovie</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>오늘의 기분에 맞는 영화를 추천해드립니다 🍿</div>",
    unsafe_allow_html=True
)

if st.button("🎲 영화 추천"):

    st.image(movie["poster"], width=260)

    st.markdown(f"""
    <div class="card">

    <h2>{movie["title"]}</h2>

    <p class="genre">🎭 {movie["genre"]}</p>

    <hr>

    <p class="story">{movie["story"]}</p>

    </div>
    """, unsafe_allow_html=True)

    st.success("즐거운 영화 감상 되세요! 🍿")
