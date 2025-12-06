import os
from typing import List

import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf


@st.cache_data
def load_tickers_from_csv(filename: str) -> List[str]:
    """Membaca daftar ticker dari CSV (kolom 'Ticker')."""
    if not os.path.exists(filename):
        return []
    try:
        df = pd.read_csv(filename)
    except Exception:
        return []

    if "Ticker" not in df.columns:
        return []

    tickers = (
        df["Ticker"]
        .astype(str).str.strip().str.upper()
        .dropna().unique().tolist()
    )
    return tickers


@st.cache_data(ttl=3600)
def fetch_stock_data(tickers: List[str], period: str = "2y") -> pd.DataFrame:
    """
    Mengunduh harga saham (Adj Close) dari Yahoo Finance.
    Mengembalikan DataFrame: kolom = ticker.YF (misalnya 'PTRO.JK').
    """
    if not tickers:
        return pd.DataFrame()

    tickers_yf = [t + ".JK" if not t.endswith(".JK") else t for t in tickers]

    data = yf.download(
        tickers_yf,
        period=period,
        group_by="ticker",
        progress=False,
        auto_adjust=False,
    )

    if data.empty:
        return pd.DataFrame()

    if isinstance(data.columns, pd.MultiIndex):
        # Struktur multi-index: (TICKER, FIELD)
        try:
            adj_close = data.xs("Adj Close", level=1, axis=1)
        except KeyError:
            adj_close = data.xs("Close", level=1, axis=1)
    else:
        adj_close = data["Adj Close"] if "Adj Close" in data else data

    adj_close.columns.name = None
    return adj_close


def compute_log_returns(price_df: pd.DataFrame) -> pd.DataFrame:
    """Menghitung log return harian: log(P_t / P_{t-1})."""
    if price_df.empty:
        return pd.DataFrame()
    return np.log(price_df / price_df.shift(1)).dropna()
