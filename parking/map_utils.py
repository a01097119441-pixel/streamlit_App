import folium
from folium.plugins import MarkerCluster


# ----------------------------------
# 무료 여부에 따른 마커 색상
# ----------------------------------
def get_marker_color(value):

    value = str(value)

    if (
        "Y" in value
        or "무료" in value
        or "가능" in value
    ):
        return "green"

    return "blue"


# ----------------------------------
# 지도 생성
# ----------------------------------
def create_map(df):

    # 데이터 없을 경우 서울시청
    if len(df) == 0:

        center = [37.5665, 126.9780]

    else:

        center = [
            df["위도"].mean(),
            df["경도"].mean()
        ]

    m = folium.Map(
        location=center,
        zoom_start=12,
        control_scale=True
    )

    cluster = MarkerCluster().add_to(m)

    for _, row in df.iterrows():

        popup = f"""
        <div style="width:260px">

        <h4>{row["주차장명"]}</h4>

        <hr>

        <b>주소</b><br>
        {row["주소"]}

        <br><br>

        <b>기본요금</b><br>
        {row["기본요금"]} 원

        <br><br>

        <b>추가요금</b><br>
        {row["추가요금"]} 원

        <br><br>

        <b>무료 여부</b><br>
        {row["무료여부"]}

        <br><br>

        <b>주말 운영</b><br>
        {row["주말운영"]}

        <br><br>

        <b>공휴일 운영</b><br>
        {row["공휴일운영"]}

        <br><br>

        <b>전화번호</b><br>
        {row["전화번호"]}

        </div>
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
                color=get_marker_color(
                    row["무료여부"]
                ),
                icon="parking",
                prefix="fa"
            )

        ).add_to(cluster)

    return m
