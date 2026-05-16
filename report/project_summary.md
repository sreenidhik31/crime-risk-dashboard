
---

```markdown
# Crime Risk & Patrol Optimization Dashboard

## Background and Introduction

This project analyzes crime incidents reported in Los Angeles from 2020 to present. The dataset contains incident-level records including crime type, date, time, area, geographic coordinates, victim attributes, and weapon-related information.

Crime data is complex because it includes temporal, categorical, and geospatial attributes. Visualization helps identify patterns that are difficult to observe from raw tables, such as crime hotspots, peak crime hours, and area-based concentration.

The purpose of this project is to create an interactive dashboard that helps users explore crime patterns and supports basic patrol decision-making.

## Key Questions to Explore

### 1. Descriptive Questions

- What are the most common types of crimes?
- Which areas have the highest number of crimes?
- How does crime frequency vary over time?

### 2. Diagnostic Questions

- Are certain crime types more common at specific times of day?
- Do specific areas consistently show higher crime rates?
- Is there a difference between weekday and weekend crime patterns?

### 3. Decision Questions

- Which areas show higher relative crime risk?
- What patrol action should be recommended based on risk level?
- Where should patrol resources be increased?

## Data Cleaning, Statistics, and Analysis

The dataset was cleaned and processed before visualization.

### Cleaning Steps

- Standardized column names
- Converted date fields into datetime format
- Removed invalid geographic coordinates such as latitude and longitude values of 0
- Extracted time features including year, month, day of week, and hour
- Created a weekend indicator

### Statistical Analysis

- Frequency count of top crime types
- Monthly crime trend analysis
- Crime distribution by day and hour
- Area-wise crime comparison
- Risk-based patrol recommendation

## Dashboard to Address Key Questions

The dashboard contains five major sections.

### 1. Crime Distribution

This section displays the most common crime categories. It answers the descriptive question of what types of crimes occur most frequently.

### 2. Temporal Analysis

This section shows monthly crime trends. It helps identify how crime frequency changes over time.

### 3. Peak Crime Timing

This section uses a day-hour heatmap to show when crime occurs most frequently. Color intensity is used to reveal high-activity time windows.

### 4. Spatial Hotspots

This section includes geospatial maps that show crime locations and density patterns.

It includes:
- Top Risk Area Hotspot Map
- Crime Density Heatmap
- Police Deployment Map

These maps help identify where crimes are concentrated and where patrols may need to be increased.

### 5. Patrol Decision System

This section converts crime frequency into normalized risk scores and patrol recommendations.

Risk Score = Area Crime Count / Maximum Area Crime Count within selected year

Decision rules:
- Risk Score ≥ 0.70 → Increase Patrol
- Risk Score 0.40–0.69 → Monitor Area
- Risk Score < 0.40 → Low Priority

The risk score is calculated across all areas within the selected year. This prevents a single selected area from automatically receiving a risk score of 1.00.

## Dashboard Design

The dashboard follows visualization design principles from the course.

- Bar charts are used for categorical crime comparison.
- Line charts are used for time-series trend analysis.
- Heatmaps use color intensity as a preattentive visual cue.
- Geospatial maps support spatial pattern recognition.
- Interactive filters allow users to explore data by year and area.
- The dashboard avoids unnecessary clutter and focuses on readable, decision-oriented visualizations.

## Summary and Conclusion

This project demonstrates how crime incident data can be transformed into meaningful visual insights.

The analysis identifies:
- common crime types
- monthly crime trends
- peak crime hours
- geographic hotspots
- high-risk patrol areas

The decision layer adds practical value by translating area-level crime frequency into patrol recommendations. This makes the dashboard useful not only for exploration but also for basic public safety resource allocation.

Overall, the project moves from understanding what happened to identifying what action should be taken.