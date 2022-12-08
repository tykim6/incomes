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
st.markdown('''
# Zip Code Targeting
## Proportional Wealth

Building on the model presented previously, I update the model to take
the *proportion* of wealthy incomes into account, as opposed to the absolute
amount. Strictly, the wealthy proportion is the ratio between the
number of returns that report incomes above $100k and the total number 
of returns (of any income level). Zip codes needed more than 5000 total
returns (of any income level) to be considered. We can adjust this (5000) number
as we see fit. 

Below is an interactive map with the top 1\% of zip codes (can also adjust this percentage)
ranked by proportional wealth. You can see the zip code as well as the relative wealth of the zip code if
you hover above the dot. The map supports dragging and zooming as well.
'''
)
st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "Zipcode: {zipcode} \nWealthy Proportion: {wealthy_prop}%"}))
