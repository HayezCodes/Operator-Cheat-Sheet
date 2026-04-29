# Shop Floor Cheat Sheet

Mobile-friendly Streamlit app for shop floor operators. This app is a clean read-only operator reference for the floor.

## Included pages
- Speeds & Feeds
- Formulas
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
