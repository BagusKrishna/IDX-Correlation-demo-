import pandas as pd
import streamlit as st

from .analysis import scan_market_correlation



def render_tab3(tickers_base, returns, windows):
    st.subheader("🔎 Scanner Pasar (All Pairs)")
    st.write("Mencari pasangan saham dengan korelasi tertinggi di seluruh market.")

    col_slider, _ = st.columns([1, 2])
    with col_slider:
        thres_scan = st.slider(
            "Minimal Korelasi (Absolut):",
            0.5, 1.0, 0.80, 0.01,
        )

    st.divider()

    scan_cols = st.columns(len(windows))
    for idx, w in enumerate(windows):
        with scan_cols[idx]:
            st.markdown(f"**📅 {w} Hari**")

            pairs = scan_market_correlation(returns, w, thres_scan)

            if pairs.empty:
                st.caption("Tidak ada hasil.")
                continue

            pairs.index.names = ["Saham A", "Saham B"]
            df_scan = pairs.to_frame(name="Correlation").reset_index()

            df_scan["Saham A"] = df_scan["Saham A"].str.replace(".JK", "", regex=False)
            df_scan["Saham B"] = df_scan["Saham B"].str.replace(".JK", "", regex=False)

            df_scan.index = df_scan.index + 1
            df_scan.index.name = "Rank"

            def color_corr(val):
                if pd.isna(val):
                    return ""
                color = "#2ecc71" if val > 0 else "#e74c3c"
                return f"color: {color}; font-weight: bold"

            styled_scan = (
                df_scan.style
                .format({"Correlation": "{:.2f}"})
                .applymap(color_corr, subset=["Correlation"])
            )

            st.dataframe(
                styled_scan,
                use_container_width=True,
            )
