import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Crime Risk Analytics & Resource Allocation Dashboard",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/crime_sample.csv", low_memory=False)
    df["date_occ"] = pd.to_datetime(df["date_occ"], errors="coerce")
    return df

df = load_data()

st.title("Crime Risk Analytics & Resource Allocation Dashboard")

st.markdown("""
This interactive dashboard analyzes Los Angeles crime incidents from 2020 to present.

It transforms large-scale crime records into temporal, geospatial, and risk-based operational insights through hotspot analysis, crime density visualization, and patrol allocation recommendations.
""")

st.sidebar.header("Dashboard Filters")

selected_year = st.sidebar.selectbox(
    "Select Year",
    sorted(df["year"].dropna().unique())
)

selected_area = st.sidebar.selectbox(
    "Select Area",
    ["All"] + sorted(df["area_name"].dropna().unique())
)

# Base year data for fair risk comparison
year_df = df[df["year"] == selected_year]

# Filtered data for dashboard charts
filtered_df = year_df.copy()

if selected_area != "All":
    filtered_df = filtered_df[filtered_df["area_name"] == selected_area]

if filtered_df.empty:
    st.warning("No data available for selected filters.")
    st.stop()

# -----------------------------
# Risk Calculation
# Always compare all areas within selected year
# -----------------------------
area_counts = year_df["area_name"].value_counts()
max_crime = area_counts.max()

risk_table = []

for area, count in area_counts.items():
    risk_score = count / max_crime if max_crime > 0 else 0

    if risk_score >= 0.70:
        action = "Increase Patrol"
    elif risk_score >= 0.40:
        action = "Monitor Area"
    else:
        action = "Low Priority"

    risk_table.append({
        "Area": area,
        "Crime Count": count,
        "Risk Score": round(risk_score, 2),
        "Recommended Action": action
    })

risk_df = pd.DataFrame(risk_table).sort_values("Risk Score", ascending=False)

st.header("Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Crimes", f"{len(filtered_df):,}")
col2.metric("Unique Crime Types", filtered_df["crm_cd_desc"].nunique())
col3.metric("Areas Covered", filtered_df["area_name"].nunique())

peak_hour = int(filtered_df["hour"].mode()[0])
col4.metric("Peak Crime Hour", f"{peak_hour}:00")

st.markdown("---")

# -----------------------------
# 1. Crime Distribution
# -----------------------------
st.header("1. Crime Distribution")

top_crimes = (
    filtered_df["crm_cd_desc"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_crimes.columns = ["Crime Type", "Count"]

fig_crimes = px.bar(
    top_crimes,
    x="Count",
    y="Crime Type",
    orientation="h",
    title="Top 10 Crime Types",
    color="Count",
    color_continuous_scale="Reds"
)

fig_crimes.update_layout(
    yaxis={"categoryorder": "total ascending"},
    xaxis_title="Crime Count",
    yaxis_title="Crime Type"
)

st.plotly_chart(fig_crimes, use_container_width=True)

top_crime = top_crimes.iloc[0]["Crime Type"]
top_crime_count = top_crimes.iloc[0]["Count"]

st.info(f"""
📌 **Insight:**  
The most frequent crime type for the selected filters is **{top_crime}** with **{top_crime_count:,} incidents**.
""")

st.markdown("---")

# -----------------------------
# 2. Temporal Analysis
# -----------------------------
st.header("2. Temporal Analysis")

monthly = (
    filtered_df
    .dropna(subset=["date_occ"])
    .groupby(filtered_df["date_occ"].dt.to_period("M"))
    .size()
    .reset_index(name="Crime Count")
)

monthly["date_occ"] = monthly["date_occ"].astype(str)

fig_monthly = px.line(
    monthly,
    x="date_occ",
    y="Crime Count",
    markers=True,
    title="Monthly Crime Trend"
)

fig_monthly.update_layout(
    xaxis_title="Month",
    yaxis_title="Crime Count"
)

st.plotly_chart(fig_monthly, use_container_width=True)

peak_month = monthly.loc[monthly["Crime Count"].idxmax(), "date_occ"]
peak_month_count = monthly["Crime Count"].max()

st.info(f"""
📌 **Insight:**  
Peak crime month for the selected filters is **{peak_month}** with **{peak_month_count:,} incidents**.
""")

st.markdown("---")

# -----------------------------
# 3. Peak Crime Timing
# -----------------------------
st.header("3. Peak Crime Timing")

day_order = [
    "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday", "Sunday"
]

day_hour = filtered_df.pivot_table(
    index="day_of_week",
    columns="hour",
    values="crm_cd_desc",
    aggfunc="count",
    fill_value=0
)

day_hour = day_hour.reindex(day_order)

fig_heatmap = px.imshow(
    day_hour,
    labels=dict(
        x="Hour of Day",
        y="Day of Week",
        color="Crime Count"
    ),
    title="Crime Frequency by Day and Hour",
    color_continuous_scale="Reds"
)

st.plotly_chart(fig_heatmap, use_container_width=True)

st.info(f"""
📌 **Insight:**  
Highest crime activity occurs around **{peak_hour}:00 hours** for the selected filters.  
This supports targeted patrol allocation during peak activity windows.
""")

st.markdown("---")

# -----------------------------
# 4. Spatial Hotspots
# -----------------------------
st.header("4. Spatial Hotspots")

st.subheader("4A. Top Risk Area Hotspot Map")

map_df = filtered_df.dropna(subset=["lat", "lon"])

if selected_area == "All":
    top_areas = risk_df.head(5)["Area"]
    map_df_top = year_df[
        year_df["area_name"].isin(top_areas)
    ].dropna(subset=["lat", "lon"])
else:
    map_df_top = map_df.copy()

if len(map_df_top) > 5000:
    map_df_top = map_df_top.sample(5000, random_state=42)

if len(map_df_top) == 0:
    st.warning("No valid latitude/longitude data available.")
else:
    fig_map = px.scatter_mapbox(
        map_df_top,
        lat="lat",
        lon="lon",
        color="area_name",
        size_max=6,
        opacity=0.5,
        hover_data=["area_name", "crm_cd_desc", "hour"],
        zoom=9,
        height=550,
        title="Top Risk Area Crime Incident Hotspots"
    )

    fig_map.update_layout(
        mapbox_style="carto-positron",
        margin={"r": 0, "t": 40, "l": 0, "b": 0}
    )

    st.plotly_chart(fig_map, use_container_width=True)

st.markdown("""
**Purpose:** This map shows spatial clustering for the highest-risk patrol areas.
""")

# -----------------------------
# 4B. Density Heatmap
# -----------------------------
st.subheader("4B. Crime Density Heatmap")

density_df = filtered_df.dropna(subset=["lat", "lon"])

if len(density_df) > 5000:
    density_df = density_df.sample(5000, random_state=42)

if len(density_df) == 0:
    st.warning("No valid location data available for density map.")
else:
    fig_density = px.density_mapbox(
        density_df,
        lat="lat",
        lon="lon",
        radius=5,
        center=dict(lat=34.05, lon=-118.24),
        zoom=9,
        mapbox_style="carto-positron",
        title="Crime Density Heatmap"
    )

    fig_density.update_layout(
        margin={"r": 0, "t": 40, "l": 0, "b": 0}
    )

    st.plotly_chart(fig_density, use_container_width=True)

st.markdown("""
**Purpose:** This density map highlights where crimes concentrate most strongly.
""")

# -----------------------------
# 4C. Police Deployment Map
# -----------------------------
st.subheader("4C. Police Deployment Map")

priority_areas = risk_df[risk_df["Recommended Action"] == "Increase Patrol"]["Area"]

if selected_area == "All":
    deployment_df = year_df[
        year_df["area_name"].isin(priority_areas)
    ].dropna(subset=["lat", "lon"])
else:
    selected_area_action = risk_df.loc[
        risk_df["Area"] == selected_area,
        "Recommended Action"
    ].iloc[0]

    if selected_area_action == "Increase Patrol":
        deployment_df = filtered_df.dropna(subset=["lat", "lon"])
    else:
        deployment_df = pd.DataFrame()

if len(deployment_df) > 5000:
    deployment_df = deployment_df.sample(5000, random_state=42)

if len(deployment_df) == 0:
    st.warning("Selected area is not classified as an Increase Patrol zone for this year.")
else:
    fig_deploy = px.scatter_mapbox(
        deployment_df,
        lat="lat",
        lon="lon",
        color="area_name",
        size=deployment_df["area_name"].map(area_counts),
        size_max=15,
        opacity=0.7,
        hover_data=["area_name", "crm_cd_desc", "hour"],
        zoom=9,
        height=550,
        title="Police Deployment Map: Patrol Priority Zones"
    )

    fig_deploy.update_layout(
        mapbox_style="carto-positron",
        margin={"r": 0, "t": 40, "l": 0, "b": 0}
    )

    st.plotly_chart(fig_deploy, use_container_width=True)

st.success("""
🚓 **Deployment Insight:**  
This map highlights areas classified as **Increase Patrol** based on normalized crime risk.
""")

st.markdown("""
**Interpretation:**
- Larger clusters → Higher crime concentration → Increased patrol needed
- Smaller clusters → Lower priority zones
""")

# -----------------------------
# 5. Patrol Decision System
# -----------------------------
st.header("5. Patrol Decision System")

st.markdown("""
Risk is calculated by comparing each area against all other areas within the selected year.  
This avoids inflated risk scores when a single area is selected.
""")

st.subheader("Top Risk Areas")
st.dataframe(risk_df.head(10), use_container_width=True)

priority_zones = risk_df[risk_df["Risk Score"] >= 0.70].head(5)

st.subheader("Priority Patrol Zones")
st.dataframe(priority_zones, use_container_width=True)

if selected_area != "All":
    selected_risk_row = risk_df[risk_df["Area"] == selected_area].iloc[0]

    st.info(f"""
📍 **Selected Area Risk:**  
For **{selected_area}**, the risk score is **{selected_risk_row["Risk Score"]}**.  
Recommended action: **{selected_risk_row["Recommended Action"]}**.
""")

top_area = risk_df.iloc[0]["Area"]
top_risk = risk_df.iloc[0]["Risk Score"]
top_action = risk_df.iloc[0]["Recommended Action"]

st.success(f"""
🚨 **Actionable Insight:**  
The highest-risk area in **{int(selected_year)}** is **{top_area}** with a risk score of **{top_risk}**.  
Recommended action: **{top_action}**.
""")

st.markdown("""
**Decision Rules:**

- **Risk Score ≥ 0.70:** Increase Patrol  
- **Risk Score 0.40–0.69:** Monitor Area  
- **Risk Score < 0.40:** Low Priority  
""")

st.markdown("---")

st.header("Summary")

st.markdown("""
This dashboard combines:

- **Descriptive analysis** to identify common crime types  
- **Temporal analysis** to detect monthly and hourly crime patterns  
- **Geospatial analysis** to locate crime hotspots  
- **Decision-oriented analytics** to recommend patrol actions  

The project moves beyond basic visualization by translating crime patterns into actionable public safety recommendations.
""")