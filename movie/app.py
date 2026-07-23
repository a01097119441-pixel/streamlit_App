import streamlit as st

st.set_page_config(page_title="MoodMovie", page_icon="🎬")

st.title("🎬 MoodMovie")
st.write("오늘의 기분에 맞는 영화를 추천해드립니다!")

movies = {
    "😊 행복": {
        "title": "인사이드 아웃",
        "genre": "애니메이션",
        "story": "기쁨, 슬픔 등 감정들이 펼치는 따뜻한 이야기."
    },
    "😢 슬픔": {
        "title": "코코",
        "genre": "애니메이션",
        "story": "가족의 소중함과 추억을 그린 감동 영화."
    },
    "😍 설렘": {
        "title": "라라랜드",
        "genre": "로맨스",
        "story": "꿈과 사랑 사이에서 고민하는 두 사람의 이야기."
    },
    "😎 액션": {
        "title": "탑건: 매버릭",
        "genre": "액션",
        "story": "최고의 파일럿이 펼치는 짜릿한 비행 액션."
    },
    "😂 웃고 싶다": {
        "title": "극한직업",
        "genre": "코미디",
        "story": "형사들이 치킨집을 운영하며 벌어지는 코미디."
    },
    "😱 무섭다": {
        "title": "곤지암",
        "genre": "공포",
        "story": "폐병원을 탐험하며 벌어지는 공포 이야기."
    }
}

mood = st.selectbox("오늘의 기분을 선택하세요.", list(movies.keys()))

if st.button("🎲 추천받기"):
    movie = movies[mood]

    st.success("추천 완료!")

    st.markdown(f"""
### 🎬 {movie['title']}

**🎭 장르** : {movie['genre']}

**📖 줄거리**

{movie['story']}
""")
