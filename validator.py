import streamlit as st
import pandas as pd
import io

# ---------------------------------------------------------
# 1. LOAD THE DATA
# ---------------------------------------------------------

df = pd.read_csv('raw_data.csv')

# ---------------------------------------------------------
# 2. STREAMLIT APP LAYOUT
# ---------------------------------------------------------
st.set_page_config(page_title="TS Data Validator", layout="wide", page_icon="ts.png")

st.title("Total Station Data Validation & Export Dashboard")
st.markdown("Streamlined digital workflow for reviewing, validating, and exporting survey data.")

# --- Section A: Data Preview ---
st.subheader("1. Raw Data Preview")
# FIX: Replaced use_container_width=True with width="stretch"
st.dataframe(df, width="stretch", height=250)

# --- Section B: Automated QA/QC Checks ---
st.subheader("2. Automated QA/QC Checks")
col1, col2, col3 = st.columns(3)

missing_desc = df['Description'].isna().sum() + (df['Description'] == '').sum()
col1.metric(
    label="Missing Descriptions", 
    value=missing_desc, 
    delta="✅ Pass" if missing_desc == 0 else "❌ Action Required",
    delta_color="normal" if missing_desc == 0 else "inverse"
)

dup_points = df['Point'].duplicated().sum()
col2.metric(
    label="Duplicate Point IDs", 
    value=dup_points, 
    delta="✅ Pass" if dup_points == 0 else "❌ Action Required",
    delta_color="normal" if dup_points == 0 else "inverse"
)

mean_elev = df['Elevation'].mean()
std_elev = df['Elevation'].std()
outliers = ((df['Elevation'] - mean_elev).abs() > (2 * std_elev)).sum()
col3.metric(
    label="Elevation Outliers (>2σ)", 
    value=int(outliers), 
    delta="✅ Pass" if outliers == 0 else "⚠️ Review",
    delta_color="normal" if outliers == 0 else "inverse"
)

# --- Section C: Spatial Visualization ---
st.subheader("3. Spatial Preview (Easting vs. Northing)")
st.scatter_chart(df, x='Easting', y='Northing', color='Description', size=100)

# --- Section D: Export ---
st.subheader("4. Export Validated Data")
st.markdown("Click below to download the cleaned and validated dataset.")

csv_export = df.to_csv(index=False).encode('utf-8')

# FIX: Replaced use_container_width=True with width="stretch"
st.download_button(
    label="📥 Download Data as CSV",
    data=csv_export,
    file_name='validated_ts_data.csv',
    mime='text/csv',
    width="stretch"
)