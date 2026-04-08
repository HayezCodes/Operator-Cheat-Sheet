from pathlib import Path

import streamlit as st


APP_ROOT = Path(__file__).resolve().parent.parent
PAGE_TARGETS = {
    "Home": APP_ROOT / "app.py",
    "Speeds & Feeds": APP_ROOT / "pages" / "1_Speeds_Feeds.py",
    "Quick Notes": APP_ROOT / "pages" / "2_Quick_Notes.py",
    "G & M Codes": APP_ROOT / "pages" / "3_G_M_Codes.py",
}


def switch_to_page(page_name: str) -> None:
    st.switch_page(PAGE_TARGETS[page_name])


def render_floor_nav(active_page: str) -> None:
    page_names = list(PAGE_TARGETS.keys())
    st.sidebar.title("Floor App")
    page = st.sidebar.radio(
        "Navigate",
        page_names,
        index=page_names.index(active_page),
    )

    if page != active_page:
        switch_to_page(page)


def render_cutting_mode_sidebar() -> None:
    modes = ["Conservative", "Standard", "Aggressive"]
    if "cut_mode" not in st.session_state:
        st.session_state["cut_mode"] = "Standard"

    current = st.session_state.get("cut_mode", "Standard")
    if current not in modes:
        current = "Standard"

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Cut Mode")
    st.session_state["cut_mode"] = st.sidebar.radio(
        "Use Mode",
        modes,
        index=modes.index(current),
        help="Conservative = backs off speed/feed. Aggressive = bumps them up. Standard = locked baseline.",
    )
    st.sidebar.caption(
        "Conservative = about 15% lower SFM and 10% lower feed. Aggressive = about 15% higher SFM and 10% higher feed."
    )
