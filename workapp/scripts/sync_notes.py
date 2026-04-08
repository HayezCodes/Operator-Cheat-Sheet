import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

FIELDS = [
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


def load_config() -> Dict:
    config_path = Path(__file__).resolve().parents[1] / "config" / "sync_config.json"
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_rows(csv_path: Path) -> List[Dict[str, str]]:
    if not csv_path.exists():
        raise FileNotFoundError(f"Notes CSV not found: {csv_path}")
    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_rows(csv_path: Path, rows: List[Dict[str, str]]) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in FIELDS})


def append_run_log(log_path: Path, row: Dict[str, str]) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    exists = log_path.exists()
    with open(log_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if not exists:
            writer.writeheader()
        writer.writerow({field: row.get(field, "") for field in FIELDS})


def find_matching_folders(job_number: str, job_roots: List[str], include_subfolders: bool) -> List[Path]:
    matches: List[Path] = []
    for root_str in job_roots:
        root = Path(root_str)
        if not root.exists():
            continue
        iterator = root.rglob("*") if include_subfolders else root.glob("*")
        for path in iterator:
            if path.is_dir() and job_number.lower() in path.name.lower():
                matches.append(path)
    return matches


def append_note_to_job_file(folder: Path, filename: str, row: Dict[str, str]) -> Path:
    note_file = folder / filename
    block = (
        "=" * 66 + "\n"
        f"Timestamp: {row.get('timestamp', '')}\n"
        f"Pending ID: {row.get('note_id', '')}\n"
        f"Job Number: {row.get('job_number', '')}\n"
        f"Part Number: {row.get('part_number', '')}\n"
        f"Machine: {row.get('machine', '')}\n"
        f"Operator: {row.get('operator', '')}\n"
        f"Category: {row.get('category', '')}\n\n"
        f"{row.get('note', '')}\n\n"
    )
    with open(note_file, "a", encoding="utf-8") as f:
        f.write(block)
    return note_file


def main() -> None:
    config = load_config()
    base_dir = Path(__file__).resolve().parents[1]
    notes_csv = (base_dir / config["notes_csv_path"]).resolve()
    log_csv = (base_dir / config["archive_synced_log"]).resolve()
    rows = load_rows(notes_csv)
    updated_rows: List[Dict[str, str]] = []

    for row in rows:
        status = (row.get("sync_status") or "").upper()
        if status == "SYNCED":
            updated_rows.append(row)
            continue

        job_number = (row.get("job_number") or "").strip()
        row["sync_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not job_number:
            row["sync_status"] = "ERROR"
            row["sync_result"] = "Missing job number"
            updated_rows.append(row)
            append_run_log(log_csv, row)
            continue

        matches = find_matching_folders(
            job_number=job_number,
            job_roots=config["job_roots"],
            include_subfolders=bool(config.get("include_subfolders", True)),
        )

        if len(matches) == 0:
            row["sync_status"] = "NO_MATCH"
            row["sync_result"] = f"No folder match found for job {job_number}"
            updated_rows.append(row)
            append_run_log(log_csv, row)
            continue

        if len(matches) > 1:
            row["sync_status"] = "MULTIPLE_MATCHES"
            row["sync_result"] = " | ".join(str(p) for p in matches[:5])
            updated_rows.append(row)
            append_run_log(log_csv, row)
            continue

        try:
            match = matches[0]
            note_file = append_note_to_job_file(match, config["job_notes_filename"], row)
            row["sync_status"] = "SYNCED"
            row["matched_folder"] = str(match)
            row["sync_result"] = f"Appended to {note_file.name}"
        except Exception as exc:  # noqa: BLE001
            row["sync_status"] = "ERROR"
            row["sync_result"] = str(exc)
        updated_rows.append(row)
        append_run_log(log_csv, row)

    write_rows(notes_csv, updated_rows)
    print("Sync complete.")


if __name__ == "__main__":
    main()
