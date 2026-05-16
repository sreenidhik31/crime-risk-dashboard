# Crime Risk & Patrol Optimization Dashboard

## Project Overview

This project analyzes Los Angeles crime incidents from 2020 to present using public crime data.

The goal is to identify spatial and temporal crime patterns and support patrol resource allocation decisions through an interactive dashboard.

## Key Questions

### Descriptive Questions
- What are the most common crime types?
- Which areas report the highest number of crimes?
- How does crime frequency change over time?

### Diagnostic Questions
- Are some crime types more common during specific times?
- Do certain areas consistently show higher crime concentration?
- Are crimes more frequent on weekdays or weekends?

### Decision Questions
- Which areas show higher relative crime risk?
- What patrol action should be recommended based on risk level?
- Where should patrol resources be increased?

## Course Alignment

This project aligns with the course modules:

- Data abstraction
- Data processing and exploratory analysis
- Human visual perception
- Common charts
- Visualization design principles
- Geospatial visualization
- Time-series visualization
- Dashboard design

## Tools Used

- Python
- Pandas
- Plotly
- Streamlit

## Dashboard Sections

1. Crime Distribution  
   Shows the most frequent crime types.

2. Temporal Analysis  
   Shows monthly crime trends.

3. Peak Crime Timing  
   Shows crime frequency by day of week and hour.

4. Spatial Hotspots  
   Includes:
   - Top Risk Area Hotspot Map
   - Crime Density Heatmap
   - Police Deployment Map

5. Patrol Decision System  
   Converts area-level crime frequency into risk scores and recommended patrol actions.

## Risk Scoring Logic

The risk score is calculated by comparing each area's crime count with the highest area crime count within the selected year.

Risk Score = Area Crime Count / Maximum Area Crime Count

### Decision Rules

- Risk Score ≥ 0.70 → Increase Patrol
- Risk Score 0.40–0.69 → Monitor Area
- Risk Score < 0.40 → Low Priority

## Project Impact

The dashboard converts raw crime records into visual and decision-oriented insights.

It supports:
- identifying high-crime areas
- detecting peak crime times
- locating spatial hotspots
- recommending patrol actions

## How to Run

Install required packages:

```bash
pip install -r requirements.txt