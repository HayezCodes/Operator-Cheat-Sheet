import pandas as pd
import streamlit as st
from data.g_m_codes import G_CODES, M_CODES, SHOP_WARNINGS
from utils.ui_helpers import render_floor_nav, switch_to_page

st.set_page_config(page_title="G & M Codes", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
<style>
[data-testid="stSidebarNav"] {display:none;}
.block-container {padding-top: 2.2rem; padding-bottom: 1.2rem;}
</style>
""", unsafe_allow_html=True)

render_floor_nav("G & M Codes")
if st.button("🏠", help="Back to Home"):
    switch_to_page("Home")

st.title("G & M Codes")
st.caption("Operator-proof reference for common code use, including tool compensation basics")

st.warning("MOST IMPORTANT: Verify machine state, active offset, spindle direction, coolant state, tool comp, and tool length before cycle start.")

search = st.text_input("Search codes or meaning", placeholder="Example: G54, coolant, thread, spindle")
machine_filter = st.selectbox("Machine Type", ["All", "Both", "Lathe", "Mill", "652 Makino", "Steady-rest family"])


def filter_df(rows):
    df = pd.DataFrame(rows)
    if search.strip():
        mask = (
            df["code"].str.contains(search, case=False, na=False)
            | df["meaning"].str.contains(search, case=False, na=False)
            | df["note"].str.contains(search, case=False, na=False)
            | df["group"].str.contains(search, case=False, na=False)
        )
        df = df[mask]
    if machine_filter != "All":
        df = df[(df["machine"] == machine_filter) | (df["machine"] == "Both")]
    return df

st.markdown("### Common G Codes")
g_df = filter_df(G_CODES)
st.dataframe(g_df, use_container_width=True, hide_index=True)

st.markdown("### Common M Codes")
m_df = filter_df(M_CODES)
st.dataframe(m_df, use_container_width=True, hide_index=True)

st.markdown("### Shop Warnings")
for warning in SHOP_WARNINGS:
    st.write(f"- {warning}")
