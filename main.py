import pandas as pd
import streamlit as st

# 데이터 불러오기 (CP949 인코딩)
df = pd.read_csv("서울시_상권분석서비스_샘플.csv", encoding="cp949")

# 열 이름 변경
df = df.rename(columns={
    "상권_구분_코드_명": "상권유형",
    "상권_코드": "상권코드",
    "상권_코드_명": "상권이름",
    "서비스_업종_코드_명": "업종",
    "당월_매출_금액": "분기매출액",
    "당월_매출_건수": "분기매출건수"
})

# 필터: 분기 선택 (디폴트는 전체)
quarters = df["상권유형"].unique().tolist() if "상권유형" in df.columns else []
selected_quarter = st.selectbox("📅 분기 선택", ["전체"] + quarters)

if selected_quarter != "전체":
    filtered_df = df[df["상권유형"] == selected_quarter]
else:
    filtered_df = df

# 메트릭 계산
total_sales = filtered_df["분기매출액"].sum() / 1e8   # 억원 단위
total_transactions = filtered_df["분기매출건수"].sum() / 1e4  # 만건 단위
unique_markets = filtered_df["상권이름"].nunique()
unique_industries = filtered_df["업종"].nunique()

# 화면 4칸 레이아웃
col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 총 분기 매출액", f"{total_sales:,.1f} 억원")
col2.metric("🛒 총 분기 거래건수", f"{total_transactions:,.1f} 만건")
col3.metric("🏙️ 분석 상권 수", f"{unique_markets:,} 개")
col4.metric("📊 업종 종류", f"{unique_industries:,} 개")
