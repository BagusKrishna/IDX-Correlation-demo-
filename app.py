import streamlit as st

from component.data_loader import (
    load_tickers_from_csv,
    fetch_stock_data,
    compute_log_returns,
)
from component.sidebar import render_sidebar
from component.tab1 import render_tab1
from component.tab2 import render_tab2
from component.tab3 import render_tab3


# KONSTANTA, CSS, main() tetap sama seperti versi terakhir kamu


# --- KONSTANTA GLOBAL ---
CSV_FILENAME = "saham_idx.csv"
WINDOWS = [20, 60, 120]
DEFAULT_PERIOD = "2y"

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="IDX Correlation Master", layout="wide")

# --- CSS GLOBAL (opsional) ---
st.markdown("""
<style>
    .stDataFrame { font-size: 14px; }
    div[data-testid="stMetricValue"] { font-size: 18px; }
</style>
""", unsafe_allow_html=True)


def main():
    st.title("🎯 IDX Correlation Master")

    # 1. LOAD UNIVERSE SAHAM
    tickers_base = load_tickers_from_csv(CSV_FILENAME)
    if not tickers_base:
        st.error(f"File {CSV_FILENAME} tidak ditemukan atau kosong atau kolom 'Ticker' tidak ada.")
        return

    # 2. SIDEBAR (termasuk credit & tombol reload)
    reload_requested = render_sidebar(total_tickers=len(tickers_base))

    if reload_requested:
        st.cache_data.clear()
        st.rerun()

    # 3. DOWNLOAD DATA & HITUNG RETURN
    with st.spinner("Mengunduh & memproses data harga..."):
        prices = fetch_stock_data(tickers_base, DEFAULT_PERIOD)
        returns = compute_log_returns(prices)

    if returns.empty:
        st.error("Gagal memproses data harga. Cek koneksi internet atau kualitas data.")
        return

    # 4. TABS
    tab1, tab2, tab3 = st.tabs([
        "🔍 Analisa Saham (Anchor)",
        "⚖️ Bandingkan 2 Saham",
        "🔎 Scanner Pasar (All Pairs)",
    ])

    with tab1:
        render_tab1(tickers_base, returns, WINDOWS)

    with tab2:
        render_tab2(tickers_base, returns, WINDOWS)

    with tab3:
        render_tab3(tickers_base, returns, WINDOWS)


if __name__ == "__main__":
    main()
