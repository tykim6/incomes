import pandas as pd
import streamlit as st
import pydeck as pdk


df = pd.read_csv("top_zips.csv")
# Define a layer to display on a map
layer = pdk.Layer(
    "ScatterplotLayer",
    df,
    pickable=True,
    opacity=0.8,
    stroked=True,
    filled=True,
    radius_scale=6,
    radius_min_pixels=2,
    line_width_min_pixels=1,
    get_position=["longitude", "latitude"],
    get_fill_color=[255, 140, 0],
    get_line_color=[0, 0, 0],
)

# Set the viewport location
view_state = pdk.ViewState(latitude=39.8283, longitude=-98.5795, zoom=3, bearing=0, pitch=0)

st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "Zipcode: {zipcode} \nWealthy Proportion: {wealthy_prop}%"}))
