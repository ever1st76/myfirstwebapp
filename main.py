# ---------------- 고객분석 탭 ----------------
with tab2:
    st.subheader("🧑‍🤝‍🧑 고객 분석")

    # 성별 매출 도넛 차트
    if "남성_매출_금액" in df.columns and "여성_매출_금액" in df.columns:
        gender_sales = {
            "남성": df["남성_매출_금액"].sum(),
            "여성": df["여성_매출_금액"].sum()
        }
        gender_df = pd.DataFrame(list(gender_sales.items()), columns=["성별", "매출액"])

        chart_gender = alt.Chart(gender_df).mark_arc(innerRadius=60).encode(
            theta=alt.Theta("매출액:Q"),
            color=alt.Color("성별:N", scale=alt.Scale(scheme="set2")),
            tooltip=["성별", "매출액"]
        ).properties(title="⚖️ 성별 매출 비율")

        st.altair_chart(chart_gender, use_container_width=True)
    else:
        st.info("성별 매출 데이터가 없습니다.")

    # 연령대 매출 막대 차트
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
        age_sales = {col.replace("연령대_", "").replace("_매출_금액", ""): df[col].sum() for col in available_age_cols}
        age_df = pd.DataFrame(list(age_sales.items()), columns=["연령대", "매출액"])

        chart_age = alt.Chart(age_df).mark_bar(color="#2196F3").encode(
            x=alt.X("연령대:N", title="연령대"),
            y=alt.Y("매출액:Q", title="매출액"),
            tooltip=["연령대", "매출액"]
        ).properties(title="📊 연령대별 매출 현황")

        st.altair_chart(chart_age, use_container_width=True)
    else:
        st.info("연령대별 매출 데이터가 없습니다.")
