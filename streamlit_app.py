import streamlit as st
import pandas as pd
from io import StringIO
import openpyxl

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:

    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_excel(uploaded_file)
    st.write(dataframe)
