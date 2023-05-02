import pandas as pd
import streamlit as st
import pydeck as pdk

# Set the viewport location
view_state = pdk.ViewState(
    latitude=39.8283, longitude=-98.5795, zoom=3, bearing=0, pitch=0
)
st.markdown(
    """
# Zip Code Targeting
## Proportional Wealth

Building on the model presented previously, I update the model to take
the *proportion* of high incomes into account, as opposed to the absolute
amount. Strictly, the high income proportion is the ratio between the
number of returns that report incomes above $100k and the total number 
of returns (of any income level). Zip codes needed more than 5000 total
returns (of any income level) to be considered. We can adjust this (5000) number
as we see fit. 

Below is an interactive map with the top zip codes
ranked by proportional high incomes. You can see the zip code as well as the relative wealth of the zip code if
you hover above the dot. The map supports dragging and zooming as well.

Update: I have filtered out all states that Verijet does not service.


"""
)

percentile = st.selectbox(
    "Which top percentile of income would you like to see?", ("1%", "5%", "10%")
)

st.write("Currently Viewing Top ", percentile)

if percentile == "1%":
    df = pd.read_csv("1p_zips.csv")
elif percentile == "5%":
    df = pd.read_csv("5p_zips.csv")
elif percentile == "10%":
    df = pd.read_csv("10p_zips.csv")


df["zipcode"] = df["zipcode"].astype(str)

# Filter options
state_list = df["state"].unique().tolist()
selected_state = st.multiselect("Filter by state:", state_list)

df = df.dropna()
# Filter the dataframe based on user input
df["zipcode"] = df["zipcode"].astype(str)
filtered_df = df.copy()

if selected_state:
    filtered_df = filtered_df[filtered_df["state"].isin(selected_state)]


if selected_state:
    # Define a layer to display on a map
    layer = pdk.Layer(
        "ScatterplotLayer",
        filtered_df,
        pickable=True,
        opacity=0.8,
        stroked=True,
        filled=True,
        radius_scale=1,
        radius_min_pixels=5,
        line_width_min_pixels=1,
        get_position=["longitude", "latitude"],
        get_fill_color=[255, 140, 0],
        get_line_color=[0, 0, 0],
    )

else:
    # Define a layer to display on a map
    layer = pdk.Layer(
        "ScatterplotLayer",
        df,
        pickable=True,
        opacity=0.8,
        stroked=True,
        filled=True,
        radius_scale=1,
        radius_min_pixels=5,
        line_width_min_pixels=1,
        get_position=["longitude", "latitude"],
        get_fill_color=[255, 140, 0],
        get_line_color=[0, 0, 0],
    )

st.pydeck_chart(
    pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={
            "text": "Zipcode: {zipcode} \nWealthy Proportion: {wealthy_prop}%\nNumber of Returns: {all}"
        },
    )
)


# Display the filtered dataframe
display_df = filtered_df[["zipcode", "state", "wealthy_prop"]"]]
st.dataframe(display_df)
