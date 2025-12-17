import streamlit as st
import pandas as pd
import pydeck as pdk
import datetime

# Set page config
st.set_page_config(layout="wide", page_title="Trips Explorer")

st.title("Trips Data Explorer")

@st.cache_data
def load_data(file):
    try:
        df = pd.read_csv(file)
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

# Sidebar for file upload
st.sidebar.header("Data Source")
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = load_data(uploaded_file)
else:
    st.sidebar.info("Using default sample data.")
    DATA_PATH = "sample/trips.csv"
    try:
        df = load_data(DATA_PATH)
    except FileNotFoundError:
        st.error("Default file not found.")
        df = None

if df is not None:
    st.header("Data Statistics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Trips", len(df))

    with col2:
        if 'duration' in df.columns:
            # Duration is likely in seconds, convert to minutes for better readability
            avg_duration = df['duration'].mean() / 60
            st.metric("Avg Duration (min)", f"{avg_duration:.2f}")
        else:
            st.metric("Avg Duration", "N/A")

    with col3:
        if 'distance' in df.columns:
            avg_dist = df['distance'].mean()
            st.metric("Avg Distance (m)", f"{avg_dist:.2f}")
        else:
            st.metric("Avg Distance", "N/A")

    with col4:
        if 'time_start' in df.columns:
            try:
                # Assuming timestamps are unix seconds
                min_ts = df['time_start'].min()
                max_ts = df['time_start'].max()

                # Check if reasonable range for seconds (e.g., > year 2000)
                # 2000-01-01 is 946684800
                if min_ts > 946684800:
                    min_time = datetime.datetime.fromtimestamp(min_ts)
                    max_time = datetime.datetime.fromtimestamp(max_ts)
                    st.write(f"**Coverage:**")
                    st.write(f"{min_time.date()} to {max_time.date()}")
                else:
                     st.write("**Coverage:**")
                     st.write("Timestamps format unknown")
            except Exception:
                 st.write("**Coverage:** Error parsing dates")
        else:
            st.write("**Coverage:** N/A")

    st.subheader("Trips Visualization")

    # Filter by city (if multiple cities exist)
    if 'city_id' in df.columns:
        unique_cities = df['city_id'].unique()
        selected_cities = st.multiselect("Filter by City ID", unique_cities, default=unique_cities)
        df_filtered = df[df['city_id'].isin(selected_cities)]
    else:
        df_filtered = df

    if not df_filtered.empty:
        # Check required columns for map
        required_cols = ["lon_start", "lat_start", "lon_end", "lat_end"]
        if all(col in df_filtered.columns for col in required_cols):
            # Create Arcs for trips

            # Define the layer to display on a map
            layer = pdk.Layer(
                "ArcLayer",
                df_filtered,
                get_source_position=["lon_start", "lat_start"],
                get_target_position=["lon_end", "lat_end"],
                get_source_color=[0, 255, 0, 160],
                get_target_color=[255, 0, 0, 160],
                auto_highlight=True,
                width_scale=0.0001,
                get_width=5, # Constant width
                width_min_pixels=2,
                width_max_pixels=10,
            )

            # Set the viewport location
            view_state = pdk.ViewState(
                longitude=df_filtered["lon_start"].mean(),
                latitude=df_filtered["lat_start"].mean(),
                zoom=11,
                pitch=50,
            )

            # Tooltip
            tooltip = {}
            if 'duration' in df_filtered.columns:
                tooltip["text"] = "Duration: {duration}s"
            if 'distance' in df_filtered.columns:
                tooltip["text"] = tooltip.get("text", "") + "\nDistance: {distance}m"

            # Render
            st.pydeck_chart(pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v9",
                initial_view_state=view_state,
                layers=[layer],
                tooltip=tooltip
            ))

            st.write(f"Showing {len(df_filtered)} trips.")
        else:
            st.warning("Data missing required coordinates for map visualization.")

        st.subheader("Data Preview")
        st.dataframe(df_filtered.head())

    else:
        st.warning("No data to display with current filters.")

else:
    st.error("Could not load data.")
