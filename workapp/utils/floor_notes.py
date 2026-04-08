import os
import pandas as pd

COLUMNS = [
    "note_id",
    "timestamp",
    "machine",
    "operator",
    "job_number",
    "part_number",
    "category",
    "note",
    "sync_status",
    "sync_time",
    "sync_result",
    "matched_folder",
]

LEGACY_COLUMNS = [
    "timestamp",
    "machine",
    "operator",
    "job_number",
    "part_number",
    "shift",
    "category",
    "note",
]


def ensure_notes_file(filepath: str) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    if not os.path.exists(filepath):
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(filepath, index=False)


def load_notes(filepath: str) -> pd.DataFrame:
    ensure_notes_file(filepath)

    try:
        df = pd.read_csv(filepath)
    except Exception:
        return pd.DataFrame(columns=COLUMNS)

    # legacy migration support
    if "shift" in df.columns and "note_id" not in df.columns:
        migrated = pd.DataFrame()
        migrated["note_id"] = [f"LEGACY_{i+1}" for i in range(len(df))]
        migrated["timestamp"] = df.get("timestamp", "")
        migrated["machine"] = df.get("machine", "")
        migrated["operator"] = df.get("operator", "")
        migrated["job_number"] = df.get("job_number", "")
        migrated["part_number"] = df.get("part_number", "")
        migrated["category"] = df.get("category", "General")
        migrated["note"] = df.get("note", "")
        migrated["sync_status"] = "PENDING"
        migrated["sync_time"] = ""
        migrated["sync_result"] = ""
        migrated["matched_folder"] = ""
        df = migrated

    for col in COLUMNS:
        if col not in df.columns:
            df[col] = ""

    return df[COLUMNS]


def save_note(filepath: str, note_data: dict) -> None:
    ensure_notes_file(filepath)
    df = load_notes(filepath)

    new_row = pd.DataFrame([note_data])
    for col in COLUMNS:
        if col not in new_row.columns:
            new_row[col] = ""

    df = pd.concat([df, new_row[COLUMNS]], ignore_index=True)
    df.to_csv(filepath, index=False)