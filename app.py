import os
import streamlit as st
from utils.ui_helpers import render_floor_nav, switch_to_page

st.set_page_config(
    page_title="Shop Floor Cheat Sheet",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
[data-testid="stSidebarNav"] {display:none;}
.block-container {padding-top: 2.0rem; padding-bottom: 1.2rem;}
.tool-card {
    border: 1px solid rgba(250,250,250,0.14);
    border-radius: 18px;
    padding: 20px 18px 16px 18px;
    background: rgba(255,255,255,0.03);
    min-height: 175px;
    box-shadow: 0 0 0 1px rgba(255,255,255,0.02) inset;
}
.tool-icon {font-size: 2rem; margin-bottom: 0.35rem;}
.tool-title {font-size: 1.15rem; font-weight: 700; margin-bottom: 0.35rem;}
.tool-text {font-size: 0.93rem; opacity: 0.92; line-height: 1.35;}
.home-head {
    border: 1px solid rgba(250,250,250,0.10);
    border-radius: 18px;
    padding: 20px 22px;
    background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.02));
}
.section-label {font-size: 1.05rem; font-weight: 700; margin-top: 0.75rem; margin-bottom: 0.6rem; opacity: 0.95;}
</style>
""",
    unsafe_allow_html=True,
)

render_floor_nav("Home")

ROOT = os.path.dirname(__file__)
logo_candidates = [
    os.path.join(ROOT, "empower_logo.png"),
    os.path.join(ROOT, "logo.png"),
    os.path.join(ROOT, "assets", "empower_logo.png"),
    os.path.join(ROOT, "assets", "logo.png"),
    os.path.join(ROOT, "data", "empower_logo.png"),
    os.path.join(ROOT, "data", "logo.png"),
]
logo_path = next((p for p in logo_candidates if os.path.exists(p)), None)
head_left, head_right = st.columns([6, 1])

with head_left:
    st.markdown(
        """
        <div class="home-head">
            <div style="font-size:0.9rem; opacity:0.8;">EMPOWER MFG</div>
            <div style="font-size:2.2rem; font-weight:800; margin-top:0.15rem;">SHOP FLOOR CHEAT SHEET</div>
            <div style="font-size:0.98rem; opacity:0.85; margin-top:0.35rem;">
                Operator floor reference for Joshua
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with head_right:
    if logo_path:
        st.image(logo_path, width=130)

st.markdown('<div class="section-label">Quick Access</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="tool-card">
            <div class="tool-icon">⚙️</div>
            <div class="tool-title">Speeds &amp; Feeds</div>
            <div class="tool-text">Exact floor-facing version of your current toolkit speeds and feeds page, including operator notes.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("OPEN SPEEDS & FEEDS", use_container_width=True):
        switch_to_page("Speeds & Feeds")

with col2:
    st.markdown(
        """
        <div class="tool-card">
            <div class="tool-icon">📝</div>
            <div class="tool-title">Quick Notes</div>
            <div class="tool-text">Fast note entry with machine dropdown, operator name, job info, and a saved log.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("OPEN QUICK NOTES", use_container_width=True):
        switch_to_page("Quick Notes")

with col3:
    st.markdown(
        """
        <div class="tool-card">
            <div class="tool-icon">📘</div>
            <div class="tool-title">G &amp; M Codes</div>
            <div class="tool-text">Clean operator reference for common G-codes, M-codes, and machine-use reminders.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("OPEN G & M CODES", use_container_width=True):
        switch_to_page("G & M Codes")