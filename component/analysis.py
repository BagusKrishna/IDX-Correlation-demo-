import numpy as np
import pandas as pd

def get_ranked_correlation(
    returns: pd.DataFrame,
    anchor_ticker: str,
    window: int,
    min_corr: float,
) -> pd.DataFrame:
    """
    Analisa per-saham:
    - Hitung korelasi antara anchor_ticker dan semua saham lain
      dalam 'window' hari terakhir.
    - Filter berdasarkan |corr| >= min_corr.
    - Urutkan dari korelasi absolut terbesar.
    - Output: index = Rank, kolom = Ticker, Correlation.
    """
    anchor_yf = anchor_ticker + ".JK"
    if anchor_yf not in returns.columns:
        return pd.DataFrame()

    data_win = returns.tail(window).dropna(axis=1, how="any")
    if anchor_yf not in data_win.columns:
        return pd.DataFrame()

    corr_series = data_win.corr()[anchor_yf].drop(anchor_yf)
    if corr_series.empty:
        return pd.DataFrame()

    abs_corr = corr_series.abs()
    mask = abs_corr >= min_corr
    corr_series = corr_series[mask]
    abs_corr = abs_corr[mask]

    if corr_series.empty:
        return pd.DataFrame()

    df = pd.DataFrame({
        "Ticker": corr_series.index.str.replace(".JK", "", regex=False),
        "Correlation": corr_series.values,
        "abs_corr": abs_corr.values,
    }).sort_values("abs_corr", ascending=False).drop(columns="abs_corr")

    df.index = np.arange(1, len(df) + 1)
    df.index.name = "Rank"

    return df[["Ticker", "Correlation"]]


def get_pair_correlation(
    returns: pd.DataFrame,
    ticker_a: str,
    ticker_b: str,
    windows,
):
    """Mengembalikan dict: {window: corr(A,B)}."""
    res = {}
    for w in windows:
        if len(returns) < w:
            continue
        data_win = returns.tail(w)
        cols = [t + ".JK" for t in [ticker_a, ticker_b]]
        if not set(cols).issubset(data_win.columns):
            res[w] = np.nan
        else:
            res[w] = data_win[cols].corr().iloc[0, 1]
    return res


def scan_market_correlation(
    returns: pd.DataFrame,
    window: int,
    threshold: float,
):
    """Cari semua pasangan saham yang punya |corr| >= threshold."""
    data_win = returns.tail(window).dropna(axis=1, how="any")
    corr_mat = data_win.corr()

    mask = np.triu(np.ones(corr_mat.shape), k=1).astype(bool)
    upper = corr_mat.where(mask)

    pairs = upper.unstack().dropna()
    pairs = pairs[pairs.abs() >= threshold]
    pairs = pairs.sort_values(key=abs, ascending=False)
    return pairs
