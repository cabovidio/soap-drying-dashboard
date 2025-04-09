
# Soap Drying Dashboard

A Streamlit app for tracking weight loss of soap bars over time.

## How to Use

1. Upload your Excel file (with one sheet per soap type).
2. Each sheet must include:
   - `Days Since Baseline`
   - `Total Loss (%)`
3. The dashboard plots retained mass over time.

### Notes
- The sheet named `template` is ignored.
- The app expects `Total Loss (%)` in full % format (e.g., 3.5 means 3.5%).

## Deploy on Streamlit Cloud
- Push this repo to GitHub
- Deploy from https://streamlit.io/cloud
