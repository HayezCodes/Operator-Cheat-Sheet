from datetime import datetime

import streamlit as st

from data.machines_data import MACHINES
from utils.floor_notes import load_notes, save_note, ensure_notes_file
from utils.ui_helpers import render_floor_nav, switch_to_page

NOTES_FILE = "data/pending_notes.csv"

st.set_page_config(page_title="Quick Notes", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
<style>
[data-testid="stSidebarNav"] {display:none;}
.block-container {padding-top: 2.2rem; padding-bottom: 1.2rem;}
</style>
""", unsafe_allow_html=True)

ensure_notes_file(NOTES_FILE)

render_floor_nav("Quick Notes")
if st.button("🏠", help="Back to Home"):
    switch_to_page("Home")

st.title("Quick Notes")
st.caption("Fast operator note entry. Notes save to local CSV for later work-PC sync.")

left, right = st.columns([1.05, 1.35])
machine_names = list(MACHINES.keys())
category_options = ["General", "Setup", "Tooling", "Program", "Offset", "Quality", "Problem"]

with left:
    st.markdown("### Add Note")
    with st.form("quick_note_form", clear_on_submit=True):
        machine = st.selectbox("Machine*", machine_names)
        operator = st.text_input("Operator", placeholder="Operator name")

        c1, c2 = st.columns(2)
        with c1:
            job_number = st.text_input("Job Number*", placeholder="Required for later sync")
        with c2:
            part_number = st.text_input("Part Number", placeholder="Optional")

        category = st.selectbox("Category", category_options)
        note = st.text_area("Quick Note*", height=180, placeholder="Type floor note here...")

        submitted = st.form_submit_button("SAVE NOTE", use_container_width=True)

        if submitted:
            if not job_number.strip():
                st.error("Job number is required.")
            elif not note.strip():
                st.error("Note text is required.")
            else:
                note_id = datetime.now().strftime("%Y%m%d%H%M%S")
                save_note(
                    NOTES_FILE,
                    {
                        "note_id": note_id,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "machine": machine,
                        "operator": operator.strip(),
                        "job_number": job_number.strip(),
                        "part_number": part_number.strip(),
                        "category": category,
                        "note": note.strip(),
                        "sync_status": "PENDING",
                        "sync_time": "",
                        "sync_result": "",
                        "matched_folder": "",
                    },
                )
                st.success(f"Note saved. Pending ID: {note_id}")
                st.rerun()

with right:
    st.markdown("### Pending / Synced Notes")
    df = load_notes(NOTES_FILE)

    f1, f2, f3, f4 = st.columns(4)
    with f1:
        machine_filter = st.selectbox("Filter by Machine", ["All"] + machine_names)
    with f2:
        category_filter = st.selectbox("Filter by Category", ["All"] + category_options)
    with f3:
        job_filter = st.text_input("Filter by Job Number")
    with f4:
        status_filter = st.selectbox("Filter by Status", ["All", "PENDING", "SYNCED", "NO_MATCH", "MULTIPLE_MATCHES", "ERROR"])

    if not df.empty:
        if machine_filter != "All":
            df = df[df["machine"] == machine_filter]
        if category_filter != "All":
            df = df[df["category"] == category_filter]
        if job_filter.strip():
            df = df[df["job_number"].fillna("").str.contains(job_filter.strip(), case=False, na=False)]
        if status_filter != "All":
            df = df[df["sync_status"] == status_filter]

        if not df.empty:
            display_columns = [
                "timestamp",
                "note_id",
                "sync_status",
                "job_number",
                "machine",
                "operator",
                "category",
                "note",
                "sync_time",
                "matched_folder",
                "sync_result",
            ]
            st.dataframe(df[display_columns], use_container_width=True, hide_index=True)
        else:
            st.info("No matching notes found.")
    else:
        st.info("No notes saved yet.")
