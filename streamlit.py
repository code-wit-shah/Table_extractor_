import streamlit as st
import pandas as pd
import json
from extractor import extract_tables_from_csv, convert_to_json_hierarchy, convert_json_to_dataframe

st.title("CSV to JSON Converter")

file = st.file_uploader("Upload a CSV file", type=["csv"])

if file is not None:
    extracted_rows = extract_tables_from_csv(file)

    if not extracted_rows.empty:
        json_output = convert_to_json_hierarchy(extracted_rows)

        st.subheader("Extracted Data in JSON Format")
        st.json(json_output)

        dataframe_from_json = convert_json_to_dataframe(json_output)

        st.subheader("Extracted Table Created from JSON")
        st.dataframe(dataframe_from_json)
    else:
        st.info("No valid data to display.")
