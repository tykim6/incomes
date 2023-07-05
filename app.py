import pandas as pd
import streamlit as st
import pydeck as pdk
import folium
from folium.plugins import Draw
import streamlit_folium as sf
import base64


# Set the viewport location
view_state = pdk.ViewState(
    latitude=39.8283, longitude=-98.5795, zoom=3, bearing=0, pitch=0
)

st.set_page_config(layout="wide")


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

# Create a folium map
m = folium.Map(location=[37.7749, -122.4194], zoom_start=4)

# Add a marker for each data point in the filtered dataframe
for _, row in filtered_df.iterrows():
    tooltip_text = f"Zipcode: {row['zipcode']} <br> Wealthy Proportion: {row['wealthy_prop']}% <br> Number of Returns: {row['all']}"
    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        tooltip=tooltip_text,
    ).add_to(m)

# Add the draw control
draw = Draw(export=True)
draw.add_to(m)

# Display the map
r = sf.components.html(m._repr_html_(), width=1000, height=500)
selected_area = st.session_state.get("selected_area", None)

# Filter the dataframe based on the drawn area
if selected_area:
    filtered_df = filtered_df[
        (filtered_df["latitude"] >= selected_area["south"])
        & (filtered_df["latitude"] <= selected_area["north"])
        & (filtered_df["longitude"] >= selected_area["west"])
        & (filtered_df["longitude"] <= selected_area["east"])
    ]


# Display the filtered dataframe
st.dataframe(filtered_df)

# Add a button to export the filtered dataframe as a CSV file
if st.button("Export CSV"):
    # Filter the dataframe based on the drawn area
    # You need to replace the coordinates in the filter with the actual coordinates from the drawn area
    south, west, north, east = 38.8, -77.2, 39.0, -76.9
    filtered_export_df = filtered_df[
        (filtered_df["latitude"] >= south)
        & (filtered_df["latitude"] <= north)
        & (filtered_df["longitude"] >= west)
        & (filtered_df["longitude"] <= east)
    ]

    # Convert the filtered dataframe to a CSV file
    csv = filtered_export_df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # Encode the CSV file to base64
    href = f'<a href="data:file/csv;base64,{b64}" download="filtered_data.csv">Download CSV File</a>'

    # Display the download link for the CSV file
    st.markdown(href, unsafe_allow_html=True)
