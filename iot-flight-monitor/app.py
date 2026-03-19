import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px 
import folium
from streamlit_folium import st_folium 

DB_PATH = "flights.db"

st.set_page_config(page_title ="IoT flight monitor dashboard", layout="wide")
st.title("IoT Flight Monitor Dashbboard (Perak airspace)")
st.caption("Live aircraft monitoring using Opensky API + SQLite + Streamlit")

def load_data():
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT *
    FROM state_vectors
    ORDER BY id DESC
    LIMIT 200
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

df = load_data()

if df.empty:     
    st.warning("No flight data available yet. Please run collector.py to fetch data first.")
    st.stop()
    
# KPI cards
col1, col2, col3 = st.columns(3)

col1.metric("Total Flights Records Loaded:  ", len(df))
col2.metric("Unique Aircrafts Detected:  ", df["icao24"].nunique())
col3.metric("Countries Detected: ", df["origin_country"].nunique())

st.divider()

# Table preview
st.subheader("Latest Flight Data: ")
st.dataframe(df, use_container_width=True)
st.divider()

# Chart 1: Aircraft count by country
st.subheader("Aircraft Count by County: ")
country_counts = df["origin_country"].value_counts().reset_index()
country_counts.columns = ["origin_country", "Count"]

fig_country = px.bar(
    country_counts,
    x = "origin_country", 
    y = "Count",
    title = "Aircraft Count by Country"
)
st.plotly_chart(fig_country, use_container_width = True)
st.divider()

# Chart 2: Altitude scatter 
st.subheader("Altitude vs Velocity: ")
df_chart = df.dropna(subset=["baro_altitude", "velocity"])

if not df_chart.empty:
    fig_alt = px.scatter(
        df_chart,
        x = "velocity",
        y = "baro_altitude",
        color = "origin_country",
        hover_data = ["callsign", "icao24"],
        title = "Velocity vs Barometric Altitude"
    )
    st.plotly_chart(fig_alt, use_container_width = True)
else:
    st.info("No altitude and velocity data available for scatter plot.")

st.divider()

# Map Visualiation 
st.subheader("Live Aircraft Map (Perak Region): ")

map_df = df.dropna(subset = ["latitude", "longitude"])

if not map_df.empty:
    m = folium.Map(location = [4.7, 101.1], zoom_start = 7)
    
    for _, row in map_df.iterrows():
        popup_text = f"""
        Callsign: {row['callsign']}<br>
        Country: {row['origin_country']}<br>
        Altitude: {row['baro_altitude']} m<br>
        Velocity: {row['velocity']} m/s
        """
        folium.Marker(
            location = [row["latitude"], row["longitude"]],
            popup = popup_text,
        ).add_to(m)

    st_folium(m, width = 1200, height = 500)

else:
    st.info("No valid Latitude and Longitude data available for map visualization.")
st.divider()

# Auto refresh note  every 30 seconds
st.info("Tip: Keep collector.py running in one terminal, and app.py running in another terminal to see live updates.")
        