"""
Soap Drying Tracker – Streamlit App
-----------------------------------

Tracks retained weight of handmade soaps over time based on Excel input files.
Generates  line plots per soap batch, showing % retained weight.

"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math
from datetime import date

st.set_page_config(layout="wide")
st.title("Soap Drying Tracker 📉🧼")

# 👇 Add version + changelog in the sidebar
__version__ = "v0.2.0"
__release_date__ = date.today().strftime("%Y-%m-%d")

changelog = """
### Changelog ({__release_date__})
- 📍 Added baseline point at Day 0 (100% retained weight)
- 🧼 Refined Y-axis behavior (min 90% unless data drops lower)
- 📈 Improved chart formatting
"""

with st.sidebar:
    st.markdown(f"**Version:** {__version__}  \n**Date:** {__release_date__}")
    with st.expander("Show changelog"):
        st.markdown(changelog)

# 👇 Now the uploader
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])


if uploaded_file:
    all_sheets = pd.read_excel(uploaded_file, sheet_name=None, engine="openpyxl")
    data_sheets = {name: df for name, df in all_sheets.items() if name.lower() != "template"}

    st.subheader("Drying Curves by Soap Type")

    fig, ax = plt.subplots()

    max_day = 0
    min_retained = 1  # Start at 100%

    for sheet_name, df in data_sheets.items():
        df = df[["Days Since Baseline", "Total Loss (%)"]].dropna()

        if df.empty:
            continue

        soap_name = all_sheets[sheet_name].iloc[0, 0]
        df["Retained (%)"] = 1 - (df["Total Loss (%)"])

        # Insert baseline point at Day 0, 100%
        if 0 not in df["Days Since Baseline"].values:
            baseline = pd.DataFrame({
                "Days Since Baseline": [0],
                "Retained (%)": [1.0]
            })
            df = pd.concat([baseline, df[["Days Since Baseline", "Retained (%)"]]], ignore_index=True)
        else:
            df = df[["Days Since Baseline", "Retained (%)"]]

        min_retained = min(min_retained, df["Retained (%)"].min())
        max_day = max(max_day, df["Days Since Baseline"].max())

        ax.plot(
            df["Days Since Baseline"],
            df["Retained (%)"],
            marker="o",
            label=str(soap_name)
        )

    max_x = max(10, math.ceil(max_day))
    ax.set_xlim(0, max_x)
    ax.xaxis.get_major_locator().set_params(integer=True)

    y_min = min(0.9, min_retained)
    ax.set_ylim(y_min, 1)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{int(y * 100)}%"))

    ax.set_xlabel("Days Since Baseline")
    ax.set_ylabel("Retained Weight (%)")
    ax.set_title("Soap Retained Weight Over Time")
    ax.grid(True)
    ax.legend()

    st.pyplot(fig)
