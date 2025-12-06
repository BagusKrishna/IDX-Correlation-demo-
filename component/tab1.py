import pandas as pd
import streamlit as st

from .analysis import get_ranked_correlation

def render_tab1(tickers_base, returns, windows):
    st.subheader("🎛️ Filter Analisa Saham")

    filter_col, _ = st.columns([1, 3])
    with filter_col:
        anchor_select = st.selectbox(
            "Pilih Saham Utama (Anchor):",
            sorted(tickers_base),
            index=0,
        )
        min_corr_tab1 = st.slider(
            "Minimal |Korelasi| (dalam absolut):",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.05,
        )

    st.markdown("---")
    st.subheader(f"📊 Hasil Korelasi dengan saham {anchor_select}")

    cols_display = st.columns(len(windows))

    for idx, w in enumerate(windows):
        with cols_display[idx]:
            st.markdown(f"**📅 {w} Hari Terakhir**")

            df_res = get_ranked_correlation(
                returns=returns,
                anchor_ticker=anchor_select,
                window=w,
                min_corr=min_corr_tab1,
            )

            if df_res.empty:
                st.caption("Tidak ada saham yang memenuhi filter.")
            else:
                def color_corr(val):
                    if pd.isna(val):
                        return ""
                    color = "#2ecc71" if val > 0 else "#e74c3c"
                    return f"color: {color}; font-weight: bold"

                styled = (
                    df_res.style
                    .format({"Correlation": "{:.2f}"})
                    .applymap(color_corr, subset=["Correlation"])
                )

                st.dataframe(
                    styled,
                    use_container_width=True,
                )
