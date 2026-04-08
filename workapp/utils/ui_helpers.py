import streamlit as st


def render_floor_nav(active_page: str) -> None:
    st.sidebar.title("Floor App")
    page = st.sidebar.radio(
        "Navigate",
        ["Home", "Speeds & Feeds", "Quick Notes", "G & M Codes"],
        index=["Home", "Speeds & Feeds", "Quick Notes", "G & M Codes"].index(active_page),
    )

    if page == "Home" and active_page != "Home":
        st.switch_page("app.py")
    elif page == "Speeds & Feeds" and active_page != "Speeds & Feeds":
        st.switch_page("pages/1_Speeds_Feeds.py")
    elif page == "Quick Notes" and active_page != "Quick Notes":
        st.switch_page("pages/2_Quick_Notes.py")
    elif page == "G & M Codes" and active_page != "G & M Codes":
        st.switch_page("pages/3_G_M_Codes.py")


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
