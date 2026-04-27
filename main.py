import pandas as pd
import streamlit as st
import altair as alt

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일 업로드", type="csv")

if uploaded_file is not None:
    # 인코딩 시도: cp949 → utf-8-sig
    try:
        df = pd.read_csv(uploaded_file, encoding="cp949")
    except UnicodeDecodeError:
        df = pd.read_csv(uploaded_file, encoding="utf-8-sig")

    # 열 이름 변경
    df = df.rename(columns={
        "상권_구분_코드_명": "상권유형",
        "상권_코드": "상권코드",
        "상권_코드_명": "상권이름",
        "서비스_업종_코드_명": "업종",
        "당월_매출_금액": "분기매출액",
        "당월_매출_건수": "분기매출건수"
    })

    # 탭 생성
    tab1, tab2 = st.tabs(["📊 매출현황", "🧑‍🤝‍🧑 고객분석"])

    # ---------------- 매출현황 탭 ----------------
    with tab1:
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

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("💰 총 분기 매출액", f"{total_sales:,.1f} 억원")
        col2.metric("🛒 총 분기 거래건수", f"{total_transactions:,.1f} 만건")
        col3.metric("🏙️ 분석 상권 수", f"{unique_markets:,} 개")
        col4.metric("📊 업종 종류", f"{unique_industries:,} 개")

        st.markdown("---")
        st.subheader("📈 메트릭별 상위 10 상권 분석")

        # 상위 10 상권별 매출액
        top_sales = (
            filtered_df.groupby("상권이름")["분기매출액"]
            .sum()
            .nlargest(10)
            .reset_index()
        )
        top_sales["분기매출액"] = top_sales["분기매출액"] / 1e8  # 억원 변환
        chart_sales = alt.Chart(top_sales).mark_bar(color="#4CAF50").encode(
            x=alt.X("분기매출액:Q", title="매출액(억원)"),
            y=alt.Y("상권이름:N", sort="-x", title="상권 이름"),
            tooltip=["상권이름", "분기매출액"]
        ).properties(title="💰 상위 10 상권 매출액")

        # 상위 10 상권별 거래건수
        top_transactions = (
            filtered_df.groupby("상권이름")["분기매출건수"]
            .sum()
            .nlargest(10)
            .reset_index()
        )
        top_transactions["분기매출건수"] = top_transactions["분기매출건수"] / 1e4  # 만건 변환
        chart_transactions = alt.Chart(top_transactions).mark_bar(color="#FF9800").encode(
            x=alt.X("분기매출건수:Q", title="거래건수(만건)"),
            y=alt.Y("상권이름:N", sort="-x", title="상권 이름"),
            tooltip=["상권이름", "분기매출건수"]
        ).properties(title="🛒 상위 10 상권 거래건수")

        st.altair_chart(chart_sales, use_container_width=True)
        st.altair_chart(chart_transactions, use_container_width=True)

    # ---------------- 고객분석 탭 ----------------
    with tab2:
        st.subheader("🧑‍🤝‍🧑 고객 분석")

        # 성별 매출 도넛 차트 (억원 변환)
        if "남성_매출_금액" in df.columns and "여성_매출_금액" in df.columns:
            gender_sales = {
                "남성": df["남성_매출_금액"].sum() / 1e8,
                "여성": df["여성_매출_금액"].sum() / 1e8
            }
            gender_df = pd.DataFrame(list(gender_sales.items()), columns=["성별", "매출액(억원)"])

            chart_gender = alt.Chart(gender_df).mark_arc(innerRadius=60).encode(
                theta=alt.Theta("매출액(억원):Q"),
                color=alt.Color("성별:N", scale=alt.Scale(scheme="set2")),
                tooltip=["성별", "매출액(억원)"]
            ).properties(title="⚖️ 성별 매출 비율 (억원)")

            st.altair_chart(chart_gender, use_container_width=True)
        else:
            st.info("성별 매출 데이터가 없습니다.")

        # 연령대 매출 막대 차트 (억원 변환)
        age_columns = [
            "연령대_10_매출_금액",
            "연령대_20_매출_금액",
            "연령대_30_매출_금액",
            "연령대_40_매출_금액",
            "연령대_50_매출_금액",
            "연령대_60_이상_매출_금액"
        ]
        available_age_cols = [col for col in age_columns if col in df.columns]

        if available_age_cols:
            age_sales = {col.replace("연령대_", "").replace("_매출_금액", ""): df[col].sum() / 1e8 for col in available_age_cols}
            age_df = pd.DataFrame(list(age_sales.items()), columns=["연령대", "매출액(억원)"])

            chart_age = alt.Chart(age_df).mark_bar(color="#2196F3").encode(
                x=alt.X("연령대:N", title="연령대"),
                y=alt.Y("매출액(억원):Q", title="매출액(억원)"),
                tooltip=["연령대", "매출액(억원)"]
            ).properties(title="📊 연령대별 매출 현황 (억원)")

            st.altair_chart(chart_age, use_container_width=True)
        else:
            st.info("연령대별 매출 데이터가 없습니다.")

else:
    st.warning("CSV 파일을 업로드해주세요.")
