import pandas as pd
import streamlit as st

df = pd.read_csv("top_zips.csv")
st.map(df)