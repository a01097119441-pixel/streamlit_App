import streamlit as st
import pandas as pd
import plotly.express as px

from youtube_comment_downloader import YoutubeCommentDownloader

from transformers import pipeline

st.set_page_config(page_title="YouTube 댓글 분석", layout="wide")
st.markdown("""
<link rel="stylesheet"
href="https://cdn.jsdelivr.net/gh/fonts-archive/NanumGothic/NanumGothic.css">

<style>

html, body, [class*="css"], .stApp{
    font-family: "Nanum Gothic", sans-serif;
}

h1,h2,h3,h4,h5,h6{
    font-family: "Nanum Gothic", sans-serif;
    font-weight:700;
}

div, p, span, label{
    font-family: "Nanum Gothic", sans-serif;
}

button{
    font-family: "Nanum Gothic", sans-serif;
}

input{
    font-family: "Nanum Gothic", sans-serif;
}

textarea{
    font-family: "Nanum Gothic", sans-serif;
}

</style>
""", unsafe_allow_html=True)

st.title("🎬 YouTube 댓글 분석기")

url = st.text_input("유튜브 URL 입력")

if st.button("분석 시작"):

    if url == "":
        st.warning("URL을 입력하세요.")
        st.stop()

    with st.spinner("댓글 가져오는 중..."):

        downloader = YoutubeCommentDownloader()

        comments = []

        for comment in downloader.get_comments_from_url(url):
            comments.append(comment)

            if len(comments) >= 300:
                break

    df = pd.DataFrame(comments)

    st.success(f"{len(df)}개의 댓글 수집 완료")

    st.dataframe(df.head())

    st.subheader("댓글 길이")

    df["length"] = df["text"].apply(len)

    fig = px.histogram(df, x="length")

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("감정 분석")

    classifier = pipeline(
        "sentiment-analysis",
        model="nlptown/bert-base-multilingual-uncased-sentiment"
    )

    results = []

    for text in df["text"]:

        try:
            result = classifier(text[:512])[0]

            results.append(result["label"])

        except:

            results.append("Unknown")

    df["sentiment"] = results

    st.dataframe(df[["text","sentiment"]])

    pie = px.pie(df, names="sentiment")

    st.plotly_chart(pie, use_container_width=True)

    st.subheader("좋아요 많은 댓글")

    top = df.sort_values("votes", ascending=False)

    st.dataframe(top[["text","votes"]].head(10))
