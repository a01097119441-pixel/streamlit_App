import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import re

st.set_page_config(
    page_title="서울시 공영주차장 안내",
    page_icon="🅿️",
    layout="wide"
)

st.title("🅿️ 서울시 공영주차장 안내")

uploaded_file = st.sidebar.file_uploader(
    "CSV 업로드",
    type="csv"
)

if uploaded_file is None:
    st.info("CSV 파일을 업로드하세요.")
    st.stop()

try:
    df = pd.read_csv(uploaded_file, encoding="utf-8")
except:
    df = pd.read_csv(uploaded_file, encoding="cp949")

# ===========================
# 컬럼 선택
# ===========================

use_cols = {
    "주차장명":"주차장명",
    "주소":"주소",
    "위도":"위도",
    "경도":"경도",
    "전화번호":"전화번호",
    "유무료구분명":"무료",
    "기본 주차 요금":"기본요금",
    "추가 단위 요금":"추가요금",
    "주말 운영 시작시각(HHMM)":"주말시작",
    "주말 운영 종료시각(HHMM)":"주말종료"
}

df = df[list(use_cols.keys())]

df = df.rename(columns=use_cols)

# ===========================
# 숫자 변환
# ===========================

df["기본요금"] = (
    df["기본요금"]
    .astype(str)
    .str.replace(",","")
)

df["추가요금"] = (
    df["추가요금"]
    .astype(str)
    .str.replace(",","")
)

df["기본요금"] = pd.to_numeric(
    df["기본요금"],
    errors="coerce"
)

df["추가요금"] = pd.to_numeric(
    df["추가요금"],
    errors="coerce"
)

df["기본요금"] = df["기본요금"].fillna(999999)
df["추가요금"] = df["추가요금"].fillna(999999)

df["위도"] = pd.to_numeric(df["위도"], errors="coerce")
df["경도"] = pd.to_numeric(df["경도"], errors="coerce")

df = df.dropna(subset=["위도","경도"])

# ===========================
# 자치구 추출
# ===========================

df["자치구"] = df["주소"].str.extract(
    r'([가-힣]+구)'
)
# ===========================
# 검색
# ===========================

st.sidebar.header("검색")

gu_list = ["전체"] + sorted(df["자치구"].unique().tolist())

selected_gu = st.sidebar.selectbox(
    "자치구 선택",
    gu_list
)

keyword = st.sidebar.text_input(
    "주소 또는 주차장명 검색"
)

free_only = st.sidebar.checkbox(
    "무료 주차장만 보기"
)

# ===========================
# 필터
# ===========================

result = df.copy()

if selected_gu != "전체":
    result = result[
        result["자치구"] == selected_gu
    ]

if keyword:

    result = result[
        result["주소"].str.contains(
            keyword,
            case=False,
            na=False
        )
        |
        result["주차장명"].str.contains(
            keyword,
            case=False,
            na=False
        )
    ]

if free_only:

    result = result[
        result["무료"]
        .astype(str)
        .str.contains("무료", na=False)
    ]

# ===========================
# 통계
# ===========================

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "주차장 수",
        len(result)
    )

with c2:

    if len(result):

        st.metric(
            "최저 기본요금",
            f"{int(result['기본요금'].min())} 원"
        )

    else:

        st.metric(
            "최저 기본요금",
            "-"
        )

with c3:

    free_count = len(

        result[
            result["무료"]
            .astype(str)
            .str.contains("무료", na=False)
        ]

    )

    st.metric(
        "무료 주차장",
        free_count
    )
    # ===========================
# 지도
# ===========================

st.subheader("🗺️ 공영주차장 위치")

if len(result) > 0:

    center = [
        result["위도"].mean(),
        result["경도"].mean()
    ]

else:

    center = [37.5665, 126.9780]

m = folium.Map(
    location=center,
    zoom_start=12,
    control_scale=True
)

cluster = MarkerCluster().add_to(m)

for _, row in result.iterrows():

    color = "blue"

    if "무료" in str(row["무료"]):
        color = "green"

    popup = f"""
    <b>{row['주차장명']}</b><br><br>

    📍 주소<br>
    {row['주소']}<br><br>

    💰 기본요금 : {int(row['기본요금'])}원<br>

    ➕ 추가요금 : {int(row['추가요금'])}원<br><br>

    🆓 {row['무료']}<br><br>

    📅 주말 운영<br>

    {row['주말시작']} ~ {row['주말종료']}<br><br>

    ☎ {row['전화번호']}
    """

    folium.Marker(

        location=[
            row["위도"],
            row["경도"]
        ],

        tooltip=row["주차장명"],

        popup=folium.Popup(
            popup,
            max_width=320
        ),

        icon=folium.Icon(
            color=color,
            icon="info-sign"
        )

    ).add_to(cluster)

st_folium(
    m,
    width=None,
    height=650
)

# ===========================
# 가장 저렴한 주차장
# ===========================

st.subheader("💰 가장 저렴한 공영주차장")

if len(result):

    cheap = result.sort_values(
        "기본요금"
    ).iloc[0]

    st.success(f"""
주차장명 : {cheap['주차장명']}

주소 : {cheap['주소']}

기본요금 : {int(cheap['기본요금'])}원

추가요금 : {int(cheap['추가요금'])}원

무료 여부 : {cheap['무료']}
""")

else:

    st.warning("검색 결과가 없습니다.")
# ===========================
# 자치구별 주차장 개수
# ===========================

st.subheader("📊 자치구별 주차장 개수")

if len(result):

    chart = (
        result.groupby("자치구")
        .size()
        .reset_index(name="주차장 수")
        .sort_values("주차장 수", ascending=False)
    )

    st.bar_chart(
        chart.set_index("자치구")
    )

# ===========================
# 검색 결과 테이블
# ===========================

st.subheader("📋 검색 결과")

show_cols = [
    "주차장명",
    "주소",
    "자치구",
    "기본요금",
    "추가요금",
    "무료",
    "주말시작",
    "주말종료",
    "전화번호"
]

st.dataframe(
    result[show_cols],
    use_container_width=True,
    hide_index=True
)

# ===========================
# CSV 다운로드
# ===========================

csv = result.to_csv(
    index=False,
    encoding="utf-8-sig"
)

st.download_button(
    label="📥 검색 결과 CSV 다운로드",
    data=csv,
    file_name="parking_result.csv",
    mime="text/csv"
)

# ===========================
# 앱 정보
# ===========================

st.markdown("---")

st.caption("🅿️ 서울시 공영주차장 정보 공유 앱")

st.caption("데이터 : 서울시 공공데이터")

st.caption("제작 : Streamlit + Folium")ㅍ

df["자치구"] = df["자치구"].fillna("기타")
