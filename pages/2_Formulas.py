import streamlit as st

from utils.ui_helpers import render_floor_nav, switch_to_page

st.set_page_config(page_title="Formulas", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
<style>
[data-testid="stSidebarNav"] {display:none;}
.block-container {padding-top: 2.2rem; padding-bottom: 1.2rem;}
</style>
""", unsafe_allow_html=True)

render_floor_nav("Formulas")
if st.button("🏠", help="Back to Home"):
    switch_to_page("Home")

st.title("Formulas")
st.caption("Empower MFG - Operator Reference")

st.info("Quick reference only. Use the app values and approved shop process first.")

with st.expander("Turning Formulas", expanded=True):
    st.markdown("### RPM from SFM")
    st.code("RPM = (SFM x 3.82) / Diameter")

    st.markdown("### Feedrate from IPR")
    st.code("IPM = RPM x IPR")

    st.markdown("### Diameter stock removal")
    st.code("Diameter removal = radial DOC x 2")

    st.markdown("### Radial DOC from diameter stock")
    st.code("Radial DOC = diameter stock removal / 2")

    st.markdown("### Surface finish estimate")
    st.code("Ra ~= Feed^2 / (32 x Nose Radius)")

    st.caption("Surface finish formula is an estimate only. Tool geometry, material, rigidity, and insert condition still matter.")

with st.expander("Milling Formulas", expanded=True):
    st.markdown("### RPM from SFM")
    st.code("RPM = (SFM x 3.82) / Tool Diameter")

    st.markdown("### Mill feedrate")
    st.code("IPM = RPM x Flutes x IPT")

    st.markdown("### Chipload")
    st.code("IPT = IPM / (RPM x Flutes)")

    st.markdown("### Quick definitions")
    st.write("ADOC = axial depth of cut")
    st.write("RDOC / WOC = radial width of cut / stepover")

    st.caption("For milling, DOC should usually be separated into axial DOC and radial WOC.")

with st.expander("Drilling & Tapping Formulas", expanded=True):
    st.markdown("### Drill RPM")
    st.code("RPM = (SFM x 3.82) / Drill Diameter")

    st.markdown("### Drill feedrate")
    st.code("IPM = RPM x IPR")

    st.markdown("### Tap feed for inch taps")
    st.code("Feed IPM = RPM / TPI")

    st.markdown("### Drill point depth estimate")
    st.code("118 deg drill point depth ~= Diameter x 0.300")
    st.code("135 deg drill point depth ~= Diameter x 0.207")

    st.caption("Tap feed must match thread pitch. Do not override rigid tapping feed unless the control/post requires it.")

st.markdown("### Quick Definitions")
definitions_left, definitions_right = st.columns(2)

with definitions_left:
    st.write("SFM = surface feet per minute")
    st.write("RPM = spindle revolutions per minute")
    st.write("IPR = inches per revolution")
    st.write("IPT = inches per tooth")
    st.write("IPM = inches per minute")

with definitions_right:
    st.write("DOC = depth of cut")
    st.write("ADOC = axial depth of cut")
    st.write("RDOC = radial depth of cut")
    st.write("WOC = width of cut / stepover")
    st.write("TPI = threads per inch")
