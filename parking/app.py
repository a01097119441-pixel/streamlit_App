import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import re

st.set_page_config(
    page_title="서울시 공영주차장",
    page_icon="🅿️",
    layout="wide"
)

st.title("🅿️ 서울시 공영주차장 안내")
st.write("서울시 공영주차장 정보를 지도에서 확인하세요.")

uploaded_file = st.sidebar.file_uploader(
    "CSV 업로드",
    type=["csv"]
)

if uploaded_file is None:
    st.info("CSV 파일을 업로드하세요.")
    st.stop()

try:
    df = pd.read_csv(uploaded_file, encoding="utf-8")
except:
    df = pd.read_csv(uploaded_file, encoding="cp949")


def find_col(keyword):

    for c in df.columns:
        if keyword in c:
            return c
    return None


name_col = find_col("주차장명")
addr_col = find_col("주소")
lat_col = find_col("위도")
lon_col = find_col("경도")
tel_col = find_col("전화")

basic_col = find_col("기본")
add_col = find_col("추가")
free_col = find_col("무료")
weekend_col = find_col("주말")


rename = {}

if name_col:
    rename[name_col] = "주차장명"

if addr_col:
    rename[addr_col] = "주소"

if lat_col:
    rename[lat_col] = "위도"

if lon_col:
    rename[lon_col] = "경도"

if tel_col:
    rename[tel_col] = "전화번호"

if basic_col:
    rename[basic_col] = "기본요금"

if add_col:
    rename[add_col] = "추가요금"

if free_col:
    rename[free_col] = "무료여부"

if weekend_col:
    rename[weekend_col] = "주말운영"

df = df.rename(columns=rename)

need = [
    "주차장명",
    "주소",
    "위도",
    "경도",
    "전화번호",
    "기본요금",
    "추가요금",
    "무료여부",
    "주말운영"
]

for c in need:
    if c not in df.columns:
        df[c] = ""


def num(x):

    if pd.isna(x):
        return 999999

    x = str(x)

    n = re.findall(r"\d+", x)

    if len(n) == 0:
        return 999999

    return int(n[0])


df["기본요금"] = df["기본요금"].apply(num)
df["추가요금"] = df["추가요금"].apply(num)

df["위도"] = pd.to_numeric(df["위도"], errors="coerce")
df["경도"] = pd.to_numeric(df["경도"], errors="coerce")

df = df.dropna(subset=["위도", "경도"])


district = []

for addr in df["주소"]:

    m = re.search(r"([가-힣]+구)", str(addr))

    if m:
        district.append(m.group(1))
    else:
        district.append("기타")

df["자치구"] = district

gu = st.sidebar.selectbox(
    "자치구",
    ["전체"] + sorted(df["자치구"].unique())
)

keyword = st.sidebar.text_input(
    "주소 검색"
)

if gu != "전체":
    df = df[df["자치구"] == gu]

if keyword:
    df = df[df["주소"].str.contains(keyword, na=False)]

st.subheader("검색 결과")

c1, c2 = st.columns(2)

with c1:
    st.metric("주차장 수", len(df))

with c2:

    if len(df):
        st.metric(
            "최저 기본요금",
            f"{df['기본요금'].min()}원"
        )
# -----------------------------
# 지도 생성
# -----------------------------

if len(df) > 0:

    center = [
        df["위도"].mean(),
        df["경도"].mean()
    ]

else:

    center = [37.5665, 126.9780]


m = folium.Map(
    location=center,
    zoom_start=12
)

cluster = MarkerCluster().add_to(m)

for _, row in df.iterrows():

    color = "blue"

    if "무료" in str(row["무료여부"]) or "Y" in str(row["무료여부"]):
        color = "green"

    popup = f"""
    <b>{row['주차장명']}</b><br><br>

    📍 주소<br>
    {row['주소']}<br><br>

    💰 기본요금<br>
    {row['기본요금']}원<br><br>

    ➕ 추가요금<br>
    {row['추가요금']}원<br><br>

    🆓 무료여부<br>
    {row['무료여부']}<br><br>

    📅 주말운영<br>
    {row['주말운영']}<br><br>

    ☎ 전화번호<br>
    {row['전화번호']}
    """

    folium.Marker(

        location=[
            row["위도"],
            row["경도"]
        ],

        tooltip=row["주차장명"],

        popup=folium.Popup(
            popup,
            max_width=300
        ),

        icon=folium.Icon(
            color=color,
            icon="info-sign"
        )

    ).add_to(cluster)

st.subheader("🗺️ 공영주차장 지도")

st_folium(
    m,
    width=None,
    height=650
)

# -----------------------------
# 가장 저렴한 주차장
# -----------------------------

st.subheader("💰 가장 저렴한 공영주차장")

if len(df) > 0:

    cheap = df.sort_values(
        "기본요금"
    ).iloc[0]

    st.success(f"""
주차장명 : {cheap['주차장명']}

주소 : {cheap['주소']}

기본요금 : {cheap['기본요금']}원

추가요금 : {cheap['추가요금']}원
""")

else:

    st.warning("검색 결과가 없습니다.")

# -----------------------------
# 무료 주차장 개수
# -----------------------------

free_count = len(

    df[
        df["무료여부"]
        .astype(str)
        .str.contains("무료|Y", na=False)
    ]

)

st.info(f"🆓 무료 주차장 : {free_count}개")

# -----------------------------
# 주말 운영 개수
# -----------------------------

weekend_count = len(

    df[
        df["주말운영"]
        .astype(str)
        .str.contains("Y|운영|가능", na=False)
    ]

)

st.info(f"📅 주말 운영 : {weekend_count}개")
# -----------------------------
# 자치구별 주차장 개수
# -----------------------------
st.subheader("📊 자치구별 공영주차장 개수")

chart_df = (
    df.groupby("자치구")
      .size()
      .reset_index(name="개수")
      .sort_values("개수", ascending=False)
)

if len(chart_df) > 0:
    st.bar_chart(
        chart_df.set_index("자치구")
    )

# -----------------------------
# 검색 결과 테이블
# -----------------------------
st.subheader("📋 검색 결과")

show_cols = []

for col in [
    "주차장명",
    "주소",
    "기본요금",
    "추가요금",
    "무료여부",
    "주말운영",
    "전화번호"
]:
    if col in df.columns:
        show_cols.append(col)

st.dataframe(
    df[show_cols],
    use_container_width=True,
    hide_index=True
)

# -----------------------------
# CSV 다운로드
# -----------------------------
csv = df.to_csv(
    index=False,
    encoding="utf-8-sig"
)

st.download_button(
    "📥 검색 결과 다운로드",
    data=csv,
    file_name="parking_result.csv",
    mime="text/csv"
)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption("서울시 공영주차장 정보 조회 앱 | Streamlit")
