import math
import streamlit as st

from data.materials import LATHE_MATERIALS, MILL_MATERIALS, DRILL_DATA, OPERATOR_NOTES
from utils.formulas import rpm_from_sfm, ipm_from_ipr, drill_feed_ipm, tap_feed_ipm_from_tpi
from utils.ui_helpers import render_cutting_mode_sidebar, render_floor_nav

st.set_page_config(
    page_title="Speeds & Feeds",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
[data-testid="stSidebarNav"] {
    display: none;
}

.block-container {
    padding-top: 2.2rem;
    padding-bottom: 1.2rem;
}

header[data-testid="stHeader"] {
    height: 0.8rem;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# CENTER DRILL PRESETS
# =========================================================
CENTER_DRILL_PRESETS = {
    "Std 00": {"style": "Standard", "pilot": 0.025000, "body": 0.1250, "C": 0.025000},
    "Std 0": {"style": "Standard", "pilot": 0.031250, "body": 0.1250, "C": 0.031250},
    "Std 1": {"style": "Standard", "pilot": 0.046875, "body": 0.1250, "C": 0.046875},
    "Std 2": {"style": "Standard", "pilot": 0.078125, "body": 0.1875, "C": 0.078125},
    "Std 3": {"style": "Standard", "pilot": 0.109375, "body": 0.2500, "C": 0.109375},
    "Std 4": {"style": "Standard", "pilot": 0.125000, "body": 0.3125, "C": 0.125000},
    "Std 5": {"style": "Standard", "pilot": 0.187500, "body": 0.4375, "C": 0.187500},
    "Std 6": {"style": "Standard", "pilot": 0.218750, "body": 0.5000, "C": 0.218750},
    "Std 7": {"style": "Standard", "pilot": 0.250000, "body": 0.6250, "C": 0.250000},
    "Std 8": {"style": "Standard", "pilot": 0.312500, "body": 0.7500, "C": 0.312500},
    "Bell 11": {"style": "Bell", "pilot": 0.046875, "body": 0.1250, "C": 0.046875},
    "Bell 12": {"style": "Bell", "pilot": 0.062500, "body": 0.1875, "C": 0.062500},
    "Bell 13": {"style": "Bell", "pilot": 0.093750, "body": 0.2500, "C": 0.093750},
    "Bell 14": {"style": "Bell", "pilot": 0.109375, "body": 0.3125, "C": 0.109375},
    "Bell 15": {"style": "Bell", "pilot": 0.156250, "body": 0.4375, "C": 0.156250},
    "Bell 16": {"style": "Bell", "pilot": 0.187500, "body": 0.5000, "C": 0.187500},
    "Bell 17": {"style": "Bell", "pilot": 0.218750, "body": 0.6250, "C": 0.218750},
    "Bell 18": {"style": "Bell", "pilot": 0.250000, "body": 0.7500, "C": 0.250000},
}

# =========================================================
# NAV / HEADER
# =========================================================
render_floor_nav("Speeds & Feeds")
render_cutting_mode_sidebar()

col_home, col_title = st.columns([1, 8])
with col_home:
    if st.button("🏠", help="Back to Home"):
        st.switch_page("app.py")

with col_title:
    st.title("Speeds & Feeds")
    st.caption("Empower MFG - Operator Version")

# =========================================================
# HELPERS
# =========================================================
def apply_cut_mode(value, kind="sfm"):
    mode = st.session_state.get("cut_mode", "Standard")

    if mode == "Conservative":
        if kind == "sfm":
            return value * 0.85
        if kind in {"ipr", "ipt"}:
            return value * 0.90
    elif mode == "Aggressive":
        if kind == "sfm":
            return value * 1.15
        if kind in {"ipr", "ipt"}:
            return value * 1.10

    return value


def get_operator_notes(material_name: str):
    if "Titanium" in material_name:
        return OPERATOR_NOTES["Titanium"]
    elif "Duplex" in material_name or "Alloy 20" in material_name:
        return OPERATOR_NOTES["Duplex"]
    elif "Hastelloy" in material_name:
        return OPERATOR_NOTES["Hastelloy"]
    elif "Steel" in material_name or "17-4" in material_name or "300" in material_name:
        return OPERATOR_NOTES["Steel"]
    else:
        return OPERATOR_NOTES["General"]


def render_operator_notes(material_name: str, title="Operator Notes"):
    notes = get_operator_notes(material_name)
    st.markdown("---")
    st.markdown(f"### {title}")
    for line in notes:
        if str(line).strip():
            st.write(line)


def get_hif_feed_data(material_name: str):
    if material_name == "10 Series Steel":
        return {
            "sfm_range": "350 - 700",
            "ipt_range": ".004 - .015",
            "axial_doc": ".008 - .016",
            "chip_thickness": ".002 - .006",
            "coolant": "No",
            "grade_note": "Steel family hi-feed starting range",
        }

    if material_name == "40 Series Steel":
        return {
            "sfm_range": "350 - 700",
            "ipt_range": ".004 - .015",
            "axial_doc": ".008 - .016",
            "chip_thickness": ".002 - .006",
            "coolant": "No",
            "grade_note": "Steel family hi-feed starting range",
        }

    if material_name == "17-4 / 300 Series":
        return {
            "sfm_range": "300 - 550",
            "ipt_range": ".004 - .0165",
            "axial_doc": ".008 - .016",
            "chip_thickness": ".002 - .006",
            "coolant": "Yes / may not be required at high speeds",
            "grade_note": "Stainless / 17-4 hi-feed starting range",
        }

    if material_name == "Duplex / Alloy 20":
        return {
            "sfm_range": "300 - 550",
            "ipt_range": ".004 - .0165",
            "axial_doc": ".008 - .016",
            "chip_thickness": ".002 - .006",
            "coolant": "Yes / may not be required at high speeds",
            "grade_note": "Use stainless-style hi-feed starting range",
        }

    if material_name == "Hastelloy":
        return {
            "sfm_range": "65 - 200",
            "ipt_range": ".004 - .015",
            "axial_doc": ".008 - .016",
            "chip_thickness": ".002 - .006",
            "coolant": "Yes",
            "grade_note": "High-temp alloy hi-feed starting range",
        }

    if material_name == "Titanium":
        return {
            "sfm_range": "85 - 200",
            "ipt_range": ".004 - .015",
            "axial_doc": ".008 - .016",
            "chip_thickness": ".002 - .006",
            "coolant": "Yes",
            "grade_note": "Titanium hi-feed starting range",
        }

    return {
        "sfm_range": "Check chart",
        "ipt_range": "Check chart",
        "axial_doc": "Check chart",
        "chip_thickness": "Check chart",
        "coolant": "Check chart",
        "grade_note": "No mapped hi-feed range",
    }


def get_center_drill_data(material_name: str):
    if material_name == "10 Series Steel":
        return {"sfm": 70, "ipr": 0.0025, "notes": "Conservative center drill baseline for 10 series steel."}
    if material_name == "40 Series Steel":
        return {"sfm": 65, "ipr": 0.0023, "notes": "Conservative center drill baseline for 40 series steel."}
    if material_name == "17-4 / 300 Series":
        return {"sfm": 45, "ipr": 0.0020, "notes": "Conservative center drill baseline for stainless / 17-4."}
    if material_name == "Duplex / Alloy 20":
        return {"sfm": 35, "ipr": 0.0018, "notes": "Conservative center drill baseline for duplex / alloy 20."}
    if material_name == "Hastelloy":
        return {"sfm": 25, "ipr": 0.0015, "notes": "Low-speed center drill baseline for Hastelloy."}
    if material_name == "Titanium":
        return {"sfm": 30, "ipr": 0.0015, "notes": "Conservative center drill baseline for titanium."}
    return {"sfm": 50, "ipr": 0.0020, "notes": "General center drill baseline."}


def render_center_drill_depth_calculator(section_key: str):
    st.markdown("---")
    st.markdown("### Center Drill Depth Calculator")

    c1, c2, c3 = st.columns(3)

    with c1:
        preset_name = st.selectbox(
            "Center Drill Size",
            list(CENTER_DRILL_PRESETS.keys()),
            key=f"{section_key}_cd_preset"
        )
        preset = CENTER_DRILL_PRESETS[preset_name]

    with c2:
        target_mode = st.selectbox(
            "Target Type",
            ["Next Drill Diameter", "Bell / Body Diameter"],
            key=f"{section_key}_cd_target_mode"
        )

    with c3:
        if target_mode == "Next Drill Diameter":
            target_value = st.number_input(
                "Next Drill Diameter (in)",
                min_value=0.0001,
                value=max(preset["pilot"] + 0.0500, 0.1250),
                step=0.0010,
                format="%.4f",
                key=f"{section_key}_cd_target_drill"
            )
        else:
            target_value = st.number_input(
                "Bell / Body Diameter Target (in)",
                min_value=0.0001,
                value=preset["body"],
                step=0.0010,
                format="%.4f",
                key=f"{section_key}_cd_target_bell"
            )

    pilot_dia = preset["pilot"]
    body_dia = preset["body"]
    drill_len = preset["C"]
    angle = 60.0
    half_angle = math.radians(angle / 2.0)

    if target_mode == "Next Drill Diameter":
        bell_dia = target_value
    else:
        bell_dia = target_value

    if bell_dia <= pilot_dia:
        st.warning("Target diameter must be larger than the center drill pilot diameter.")
        return

    chamfer_depth = (bell_dia - pilot_dia) / (2 * math.tan(half_angle))
    pilot_hole_depth = chamfer_depth + drill_len

    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Pilot Dia", f"{pilot_dia:.4f}")
    r2.metric("Body / Bell Dia", f"{body_dia:.4f}")
    r3.metric("Drill Length (C)", f"{drill_len:.4f}")
    r4.metric("Recommended Depth", f"{pilot_hole_depth:.4f}")

    if bell_dia > body_dia:
        st.warning("Target diameter exceeds tool body / bell diameter.")
    else:
        st.info("Recommended depth is based on 60° included angle geometry and the tool C length.")

    st.write("Go deep enough to fully start the next drill. Do not bury the center drill deeper than needed.")

# =========================================================
# MAIN TABS
# =========================================================
main_tab1, main_tab2 = st.tabs(["Lathe", "Mill"])

# =========================================================
# LATHE
# =========================================================
with main_tab1:
    lathe_tab1, lathe_tab2, lathe_tab3, lathe_tab4 = st.tabs(
        ["Turning", "Drilling", "Live Tooling Endmill", "Live Tooling Drill"]
    )

    with lathe_tab1:
        st.subheader("Lathe Turning")
        col1, col2, col3 = st.columns(3)

        with col1:
            material = st.selectbox("Material", list(LATHE_MATERIALS.keys()), key="lathe_material")
        with col2:
            operation = st.selectbox("Operation", ["rough", "finish"], key="lathe_operation")
        with col3:
            diameter = st.number_input(
                "Work Diameter (in)",
                min_value=0.001,
                value=2.000,
                step=0.100,
                format="%.3f",
                key="lathe_dia"
            )

        rec = LATHE_MATERIALS[material][operation]
        sfm = apply_cut_mode(rec["sfm"], "sfm")
        ipr = apply_cut_mode(rec["ipr"], "ipr")
        rpm = rpm_from_sfm(sfm, diameter)
        ipm = ipm_from_ipr(ipr, rpm)

        st.markdown("### Recommendation")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("SFM", f"{sfm:.0f}")
        c2.metric("RPM", f"{rpm:.0f}")
        c3.metric("Feed (IPR)", f"{ipr:.4f}")
        c4.metric("Feed (IPM)", f"{ipm:.2f}")

        st.markdown("### Setup Guidance")
        g1, g2 = st.columns(2)
        g1.metric("DOC Guidance", rec["doc"])
        g2.markdown(
            f"""
<div style="font-size:0.90rem; line-height:1.40;">
<b>Chipbreaker:</b><br>{rec["chipbreaker"]}
</div>
""",
            unsafe_allow_html=True,
        )

        st.write(f"**Notes:** {rec['notes']}")
        render_operator_notes(material)

    with lathe_tab2:
        st.subheader("Lathe Drilling")

        col1, col2, col3 = st.columns(3)
        with col1:
            material_drill = st.selectbox("Material", list(DRILL_DATA.keys()), key="lathe_drill_material")
        with col2:
            drill_type = st.selectbox(
                "Drill Type",
                ["HSS", "HSS Coated", "Cobalt", "CoroDrill", "Center Drill"],
                key="lathe_drill_type"
            )
        with col3:
            drill_label = "Center Drill Pilot Diameter (in)" if drill_type == "Center Drill" else "Drill Diameter (in)"
            drill_diameter = st.number_input(
                drill_label,
                min_value=0.001,
                value=0.1250 if drill_type == "Center Drill" else 0.5000,
                step=0.0010 if drill_type == "Center Drill" else 0.0100,
                format="%.4f",
                key="lathe_drill_dia"
            )

        if drill_type == "Center Drill":
            drill_rec = get_center_drill_data(material_drill)
        else:
            drill_rec = DRILL_DATA[material_drill][drill_type]

        sfm = apply_cut_mode(drill_rec["sfm"], "sfm")
        ipr = apply_cut_mode(drill_rec["ipr"], "ipr")
        rpm = rpm_from_sfm(sfm, drill_diameter)
        ipm = drill_feed_ipm(rpm, ipr)

        st.markdown("### Drill Recommendation")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("SFM", f"{sfm:.0f}")
        c2.metric("RPM", f"{rpm:.0f}")
        c3.metric("Feed (IPR)", f"{ipr:.4f}")
        c4.metric("Feed (IPM)", f"{ipm:.2f}")

        st.write(f"**Notes:** {drill_rec['notes']}")

        if drill_type == "Center Drill":
            render_center_drill_depth_calculator("lathe_drilling")

        render_operator_notes(material_drill)

    with lathe_tab3:
        st.subheader("Lathe Live Tooling Endmill")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            material_live = st.selectbox("Material", list(MILL_MATERIALS.keys()), key="lathe_live_material")
        with col2:
            tool_style_live = st.selectbox(
                "Tool Style",
                ["Standard Endmill", "1/2 Ingersoll Rougher (Hi-Feed)"],
                key="lathe_live_tool_style"
            )
        with col3:
            flute_count_live = st.number_input("Flute Count", min_value=1, value=4, step=1, key="lathe_live_flutes")
        with col4:
            em_operation_live = st.selectbox("Operation", ["rough", "finish"], key="lathe_live_op")

        if tool_style_live == "1/2 Ingersoll Rougher (Hi-Feed)":
            tool_diameter_live = 0.5000
        else:
            tool_diameter_live = st.number_input(
                "Endmill Diameter (in)",
                min_value=0.001,
                value=0.5000,
                step=0.0100,
                format="%.4f",
                key="lathe_live_em_dia"
            )

        st.write(f"**Diameter Used:** {tool_diameter_live:.4f} in")

        if tool_style_live == "1/2 Ingersoll Rougher (Hi-Feed)":
            hif = get_hif_feed_data(material_live)

            st.markdown("### Live Tooling Recommendation - HI-FEED INSERT MILL")
            c1, c2, c3 = st.columns(3)
            c1.metric("SFM Range", hif["sfm_range"])
            c2.metric("IPT Range", hif["ipt_range"])
            c3.metric("Axial DOC", hif["axial_doc"])

            d1, d2, d3 = st.columns(3)
            d1.metric("Chip Thickness", hif["chip_thickness"])
            d2.metric("Coolant", hif["coolant"])
            d3.metric("Tool", "1/2 Ingersoll Rougher")

            st.write(f"**Chart Note:** {hif['grade_note']}")
            st.write("**Application Note:** Use for keyways larger than .500 when using the hi-feed insert mill.")
            st.write("**Mode Note:** This chart is a roughing / hi-feed style recommendation.")
            render_operator_notes(material_live)
        else:
            rec_live = MILL_MATERIALS[material_live]["Endmill"]

            if em_operation_live == "rough":
                sfm_live = apply_cut_mode(rec_live["rough_sfm"], "sfm")
                ipt_live = apply_cut_mode(rec_live["rough_ipt"], "ipt")
                slot_doc_live = rec_live["rough_slot_doc_factor"] * tool_diameter_live
                side_doc_live = rec_live["rough_side_doc_factor"] * tool_diameter_live
                finish_note_live = rec_live["finish_radial"]
            else:
                sfm_live = apply_cut_mode(rec_live["finish_sfm"], "sfm")
                ipt_live = apply_cut_mode(rec_live["finish_ipt"], "ipt")
                slot_doc_live = rec_live["finish_slot_doc_factor"] * tool_diameter_live
                side_doc_live = rec_live["finish_side_doc_factor"] * tool_diameter_live
                finish_note_live = rec_live["finish_radial"]

            rpm_live = rpm_from_sfm(sfm_live, tool_diameter_live)
            ipm_live = rpm_live * flute_count_live * ipt_live

            st.markdown(f"### Live Tooling Recommendation - {em_operation_live.upper()}")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("SFM", f"{sfm_live:.0f}")
            c2.metric("RPM", f"{rpm_live:.0f}")
            c3.metric("Chipload (IPT)", f"{ipt_live:.4f}")
            c4.metric("Feed (IPM)", f"{ipm_live:.2f}")

            st.markdown("### DOC Guidance")
            d1, d2, d3 = st.columns(3)
            d1.metric("Slot DOC", f"{slot_doc_live:.4f}")
            d2.metric("Side DOC", f"{side_doc_live:.4f}")
            d3.metric("Finish Radial", finish_note_live)

            st.write(f"**Notes:** {rec_live['notes']}")
            render_operator_notes(material_live)

    with lathe_tab4:
        st.subheader("Lathe Live Tooling Drill")

        col1, col2, col3 = st.columns(3)
        with col1:
            material_live_drill = st.selectbox("Material", list(DRILL_DATA.keys()), key="lathe_live_drill_material")
        with col2:
            drill_type_live = st.selectbox(
                "Drill Type",
                ["HSS", "HSS Coated", "Cobalt", "CoroDrill", "Center Drill"],
                key="lathe_live_drill_type"
            )
        with col3:
            drill_label_live = "Center Drill Pilot Diameter (in)" if drill_type_live == "Center Drill" else "Drill Diameter (in)"
            drill_diameter_live = st.number_input(
                drill_label_live,
                min_value=0.001,
                value=0.1250 if drill_type_live == "Center Drill" else 0.5000,
                step=0.0010 if drill_type_live == "Center Drill" else 0.0100,
                format="%.4f",
                key="lathe_live_drill_dia"
            )

        if drill_type_live == "Center Drill":
            drill_rec_live = get_center_drill_data(material_live_drill)
        else:
            drill_rec_live = DRILL_DATA[material_live_drill][drill_type_live]

        sfm_live = apply_cut_mode(drill_rec_live["sfm"], "sfm")
        ipr_live = apply_cut_mode(drill_rec_live["ipr"], "ipr")
        rpm_live = rpm_from_sfm(sfm_live, drill_diameter_live)
        ipm_live = drill_feed_ipm(rpm_live, ipr_live)

        st.markdown("### Live Tooling Drill Recommendation")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("SFM", f"{sfm_live:.0f}")
        c2.metric("RPM", f"{rpm_live:.0f}")
        c3.metric("Feed (IPR)", f"{ipr_live:.4f}")
        c4.metric("Feed (IPM)", f"{ipm_live:.2f}")

        st.write(f"**Notes:** {drill_rec_live['notes']}")

        if drill_type_live == "Center Drill":
            render_center_drill_depth_calculator("lathe_live_drilling")

        render_operator_notes(material_live_drill)

# =========================================================
# MILL
# =========================================================
with main_tab2:
    st.subheader("Mill Speeds & Feeds")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        material_mill = st.selectbox("Material", list(MILL_MATERIALS.keys()), key="mill_material")
    with col2:
        tool_type = st.selectbox("Tool Type", ["Spot Drill", "Center Drill", "Drill", "Tap", "Endmill"], key="mill_tool_type")
    with col3:
        if tool_type == "Endmill":
            em_operation = st.selectbox("Operation", ["rough", "finish"], key="mill_em_operation")
            drill_type_mill = None
            tool_style_mill = st.selectbox(
                "Tool Style",
                ["Standard Endmill", "1/2 Ingersoll Rougher (Hi-Feed)"],
                key="mill_tool_style"
            )
        elif tool_type == "Drill":
            drill_type_mill = st.selectbox(
                "Drill Type",
                ["HSS", "HSS Coated", "Cobalt", "CoroDrill"],
                key="mill_drill_type"
            )
            em_operation = None
            tool_style_mill = None
        else:
            em_operation = None
            drill_type_mill = None
            tool_style_mill = None
            st.write("")
    with col4:
        if tool_type == "Spot Drill":
            diameter = st.number_input(
                "Spot Drill Diameter (in)",
                min_value=0.001,
                value=0.1250,
                step=0.0100,
                format="%.4f",
                key="spot_dia"
            )
            tool_label = "Custom Spot Drill"
        elif tool_type == "Center Drill":
            diameter = st.number_input(
                "Center Drill Pilot Diameter (in)",
                min_value=0.001,
                value=0.1250,
                step=0.0010,
                format="%.4f",
                key="center_drill_dia"
            )
            tool_label = "Center Drill"
        elif tool_type == "Drill":
            diameter = st.number_input(
                "Drill Diameter (in)",
                min_value=0.001,
                value=0.5000,
                step=0.0100,
                format="%.4f",
                key="mill_drill_dia"
            )
            tool_label = "Custom Drill"
        elif tool_type == "Endmill":
            if tool_style_mill == "1/2 Ingersoll Rougher (Hi-Feed)":
                diameter = 0.5000
            else:
                diameter = st.number_input(
                    "Endmill Diameter (in)",
                    min_value=0.001,
                    value=0.5000,
                    step=0.0100,
                    format="%.4f",
                    key="mill_em_dia"
                )
            tool_label = tool_style_mill
        else:
            diameter = st.number_input(
                "Tap Diameter (in)",
                min_value=0.001,
                value=0.5000,
                step=0.0100,
                format="%.4f",
                key="tap_diameter"
            )
            tool_label = "Custom Tap Diameter"

    st.write(f"**Selected Tool:** {tool_label}")
    st.write(f"**Diameter Used:** {diameter:.4f} in")

    st.markdown("### Recommendation")

    if tool_type == "Spot Drill":
        rec = MILL_MATERIALS[material_mill]["Spot Drill"]
        sfm = apply_cut_mode(rec["sfm"], "sfm")
        ipr = apply_cut_mode(rec["ipr"], "ipr")
        rpm = rpm_from_sfm(sfm, diameter)
        ipm = drill_feed_ipm(rpm, ipr)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("SFM", f"{sfm:.0f}")
        c2.metric("RPM", f"{rpm:.0f}")
        c3.metric("Feed Basis (IPR)", f"{ipr:.4f}")
        c4.metric("Feed (IPM)", f"{ipm:.2f}")

        st.write(f"**Notes:** {rec['notes']}")
        render_operator_notes(material_mill)

    elif tool_type == "Center Drill":
        rec = get_center_drill_data(material_mill)
        sfm = apply_cut_mode(rec["sfm"], "sfm")
        ipr = apply_cut_mode(rec["ipr"], "ipr")
        rpm = rpm_from_sfm(sfm, diameter)
        ipm = drill_feed_ipm(rpm, ipr)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("SFM", f"{sfm:.0f}")
        c2.metric("RPM", f"{rpm:.0f}")
        c3.metric("Feed Basis (IPR)", f"{ipr:.4f}")
        c4.metric("Feed (IPM)", f"{ipm:.2f}")

        st.write(f"**Notes:** {rec['notes']}")
        render_center_drill_depth_calculator("mill_center_drill")
        render_operator_notes(material_mill)

    elif tool_type == "Drill":
        drill_rec = DRILL_DATA[material_mill][drill_type_mill]
        sfm = apply_cut_mode(drill_rec["sfm"], "sfm")
        ipr = apply_cut_mode(drill_rec["ipr"], "ipr")
        rpm = rpm_from_sfm(sfm, diameter)
        ipm = drill_feed_ipm(rpm, ipr)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("SFM", f"{sfm:.0f}")
        c2.metric("RPM", f"{rpm:.0f}")
        c3.metric("Feed (IPR)", f"{ipr:.4f}")
        c4.metric("Feed (IPM)", f"{ipm:.2f}")

        st.write(f"**Notes:** {drill_rec['notes']}")
        render_operator_notes(material_mill)

    elif tool_type == "Tap":
        rec = MILL_MATERIALS[material_mill]["Tap"]
        sfm = apply_cut_mode(rec["sfm"], "sfm")
        rpm = rpm_from_sfm(sfm, diameter)
        tpi = st.number_input("TPI (for inch taps)", min_value=1, value=13, step=1, key="mill_tap_tpi")
        tap_feed = tap_feed_ipm_from_tpi(rpm, tpi)

        c1, c2, c3 = st.columns(3)
        c1.metric("SFM", f"{sfm:.0f}")
        c2.metric("RPM", f"{rpm:.0f}")
        c3.metric("Feed (IPM)", f"{tap_feed:.2f}")

        st.write(f"**Notes:** {rec['notes']}")
        render_operator_notes(material_mill)

    elif tool_type == "Endmill":
        if tool_style_mill == "1/2 Ingersoll Rougher (Hi-Feed)":
            hif = get_hif_feed_data(material_mill)

            st.markdown("### Endmill Recommendation - HI-FEED INSERT MILL")
            c1, c2, c3 = st.columns(3)
            c1.metric("SFM Range", hif["sfm_range"])
            c2.metric("IPT Range", hif["ipt_range"])
            c3.metric("Axial DOC", hif["axial_doc"])

            d1, d2, d3 = st.columns(3)
            d1.metric("Chip Thickness", hif["chip_thickness"])
            d2.metric("Coolant", hif["coolant"])
            d3.metric("Tool", "1/2 Ingersoll Rougher")

            st.write(f"**Chart Note:** {hif['grade_note']}")
            st.write("**Application Note:** Use for keyways larger than .500 when using the hi-feed insert mill.")
            st.write("**Mode Note:** This chart is a roughing / hi-feed style recommendation.")
            render_operator_notes(material_mill)
        else:
            rec = MILL_MATERIALS[material_mill]["Endmill"]
            flute_count = st.number_input("Flute Count", min_value=1, value=4, step=1, key="mill_flutes")

            if em_operation == "rough":
                sfm = apply_cut_mode(rec["rough_sfm"], "sfm")
                ipt = apply_cut_mode(rec["rough_ipt"], "ipt")
                slot_doc = rec["rough_slot_doc_factor"] * diameter
                side_doc = rec["rough_side_doc_factor"] * diameter
                finish_note = rec["finish_radial"]
            else:
                sfm = apply_cut_mode(rec["finish_sfm"], "sfm")
                ipt = apply_cut_mode(rec["finish_ipt"], "ipt")
                slot_doc = rec["finish_slot_doc_factor"] * diameter
                side_doc = rec["finish_side_doc_factor"] * diameter
                finish_note = rec["finish_radial"]

            rpm = rpm_from_sfm(sfm, diameter)
            ipm = rpm * flute_count * ipt

            st.markdown(f"### Endmill Recommendation - {em_operation.upper()}")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("SFM", f"{sfm:.0f}")
            c2.metric("RPM", f"{rpm:.0f}")
            c3.metric("Chipload (IPT)", f"{ipt:.4f}")
            c4.metric("Feed (IPM)", f"{ipm:.2f}")

            st.markdown("### DOC Guidance")
            d1, d2, d3 = st.columns(3)
            d1.metric("Slot DOC", f"{slot_doc:.4f}")
            d2.metric("Side DOC", f"{side_doc:.4f}")
            d3.metric("Finish Radial", finish_note)

            st.write(f"**Notes:** {rec['notes']}")
            render_operator_notes(material_mill)
