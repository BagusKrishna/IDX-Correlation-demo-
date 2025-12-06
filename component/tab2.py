import numpy as np
import pandas as pd
import streamlit as st

from .analysis import get_pair_correlation

def render_tab2(tickers_base, returns, windows):
    st.subheader("⚖️ Bandingkan 2 Saham")

    col_filter, _ = st.columns([1, 3])
    with col_filter:
        stock_a = st.selectbox(
            "Saham A:",
            sorted(tickers_base),
            index=0,
            key="sa",
        )
        stock_b = st.selectbox(
            "Saham B:",
            sorted(tickers_base),
            index=1,
            key="sb",
        )

    st.markdown("---")

    if stock_a == stock_b:
        st.warning("⚠️ Pilih dua saham berbeda untuk dibandingkan.")
        return

    res_pair = get_pair_correlation(returns, stock_a, stock_b, windows)

    st.subheader(f"📊 Hasil Korelasi {stock_a} vs {stock_b}")

    cols_metrics = st.columns(len(windows))
    for i, w in enumerate(windows):
        val = res_pair.get(w, np.nan)
        with cols_metrics[i]:
            st.metric(
                label=f"{w} Hari",
                value=f"{val:.2f}" if not pd.isna(val) else "N/A",
                delta=(
                    "Positif" if val > 0.5
                    else "Negatif" if val < -0.5
                    else "Netral"
                ) if not pd.isna(val) else "",
            )
