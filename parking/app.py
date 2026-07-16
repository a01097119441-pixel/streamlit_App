import pandas as pd
import re


# ----------------------------
# 컬럼 자동 찾기
# ----------------------------
def find_column(df, keywords):

    for col in df.columns:
        for key in keywords:
            if key in col:
                return col

    return None


# ----------------------------
# 숫자만 추출
# ----------------------------
def extract_number(value):

    if pd.isna(value):
        return None

    value = str(value)

    nums = re.findall(r"\d+", value)

    if len(nums) == 0:
        return None

    return int(nums[0])


# ----------------------------
# 데이터 불러오기
# ----------------------------
def load_data(file):

    try:
        df = pd.read_csv(file, encoding="utf-8")

    except:

        df = pd.read_csv(file, encoding="cp949")

    # 컬럼 자동 찾기
    name_col = find_column(df, ["주차장명"])
    addr_col = find_column(df, ["주소"])
    lat_col = find_column(df, ["위도"])
    lon_col = find_column(df, ["경도"])
    tel_col = find_column(df, ["전화"])

    basic_col = find_column(df, ["기본요금"])
    add_col = find_column(df, ["추가요금"])

    free_col = find_column(df, ["무료"])
    weekend_col = find_column(df, ["주말"])
    holiday_col = find_column(df, ["공휴일"])

    # 이름 통일
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

    if holiday_col:
        rename[holiday_col] = "공휴일운영"

    df = df.rename(columns=rename)

    # 없는 컬럼 생성
    needed = [
        "주차장명",
        "주소",
        "위도",
        "경도",
        "전화번호",
        "기본요금",
        "추가요금",
        "무료여부",
        "주말운영",
        "공휴일운영",
    ]

    for col in needed:

        if col not in df.columns:
            df[col] = ""

    # 요금 숫자 변환
    df["기본요금"] = df["기본요금"].apply(extract_number)

    df["추가요금"] = df["추가요금"].apply(extract_number)

    df["기본요금"] = df["기본요금"].fillna(999999)

    df["추가요금"] = df["추가요금"].fillna(999999)

    # 위경도
    df["위도"] = pd.to_numeric(df["위도"], errors="coerce")

    df["경도"] = pd.to_numeric(df["경도"], errors="coerce")

    df = df.dropna(subset=["위도", "경도"])

    # 자치구 생성
    districts = []

    for addr in df["주소"]:

        if pd.isna(addr):
            districts.append("기타")
            continue

        text = str(addr)

        m = re.search(r"서울특별시\s*([가-힣]+구)", text)

        if m:

            districts.append(m.group(1))

        else:

            m = re.search(r"([가-힣]+구)", text)

            if m:
                districts.append(m.group(1))
            else:
                districts.append("기타")

    df["자치구"] = districts

    return df


# ----------------------------
# 자치구
# ----------------------------
def get_districts(df):

    return sorted(df["자치구"].dropna().unique())


# ----------------------------
# 필터
# ----------------------------
def filter_data(
    df,
    district="전체",
    keyword="",
    free_only=False,
    weekend_only=False,
    holiday_only=False,
):

    result = df.copy()

    if district != "전체":

        result = result[result["자치구"] == district]

    if keyword:

        result = result[
            result["주소"].str.contains(
                keyword,
                case=False,
                na=False
            )
        ]

    if free_only:

        result = result[
            result["무료여부"].astype(str).str.contains(
                "Y|무료|가능",
                case=False,
                na=False
            )
        ]

    if weekend_only:

        result = result[
            result["주말운영"].astype(str).str.contains(
                "Y|가능|운영",
                case=False,
                na=False
            )
        ]

    if holiday_only:

        result = result[
            result["공휴일운영"].astype(str).str.contains(
                "Y|가능|운영",
                case=False,
                na=False
            )
        ]

    return result


# ----------------------------
# 가장 저렴한 주차장
# ----------------------------
def get_cheapest_parking(df):

    if len(df) == 0:
        return None

    result = df.sort_values(
        "기본요금",
        ascending=True
    )

    return result.iloc[0]
