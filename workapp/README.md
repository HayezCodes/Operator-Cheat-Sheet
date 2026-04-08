# Shop Floor Cheat Sheet

Mobile-friendly Streamlit app for shop floor operators.

## Included pages
- Speeds & Feeds
- Quick Notes
- G & M Codes

## Local run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Community Cloud
1. Create a new GitHub repository.
2. Upload the contents of this folder to the root of the repo.
3. Make sure these files stay in the repo root:
   - `app.py`
   - `requirements.txt`
   - `pages/`
   - `data/`
   - `utils/`
4. In Streamlit Community Cloud, create a new app and point it to `app.py`.

## Notes storage
Quick Notes are saved to `data/floor_notes.csv`.
If you redeploy from GitHub, new notes made in the cloud app are not a durable database. For long-term shared note retention, move notes to a real database later.


## Pending note sync workflow

Quick Notes now save into `data/pending_notes.csv` with a sync status field.

To push notes into real job folders on the work PC:

1. Edit `config/sync_config.json`
2. Set your real `job_roots`
3. Run:

```bash
python scripts/sync_notes_to_job_folders.py
```

The script searches folder names for the entered job number and appends the note into `JOB NOTES.txt` in the matching folder.
