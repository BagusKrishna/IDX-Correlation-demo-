import streamlit as st


def render_sidebar(total_tickers: int) -> bool:
    """
    Render sidebar:
    - info universe
    - tombol reload
    - credit di bagian bawah
    Mengembalikan True jika tombol reload ditekan.
    """
    st.sidebar.header("📥 Data Feed")
    st.sidebar.caption(f"Universe: {total_tickers} Saham")

    reload_button = st.sidebar.button("🔄 Reload Data")

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "<div style='font-size: 12px; color: #888;'>Made by <b>@cubeil</b></div>",
        unsafe_allow_html=True,
    )

    return reload_button
