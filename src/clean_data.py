import pandas as pd
import os


RAW_PATH = "data/raw/crime_data.csv"
PROCESSED_PATH = "data/processed/crime_cleaned.csv"


def load_data(path=RAW_PATH, sample_size=None):
    if sample_size:
        return pd.read_csv(path, nrows=sample_size, low_memory=False)
    return pd.read_csv(path, low_memory=False)


def clean_crime_data(df):
    df = df.copy()

    # Standardize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    # Convert dates
    if "date_occ" in df.columns:
        df["date_occ"] = pd.to_datetime(df["date_occ"], errors="coerce")

    if "date_rptd" in df.columns:
        df["date_rptd"] = pd.to_datetime(df["date_rptd"], errors="coerce")

    # Remove invalid coordinates
    if "lat" in df.columns and "lon" in df.columns:
        df = df[(df["lat"].notna()) & (df["lon"].notna())]
        df = df[(df["lat"] != 0) & (df["lon"] != 0)]

    # Feature engineering for time-series analysis
    if "date_occ" in df.columns:
        df["year"] = df["date_occ"].dt.year
        df["month"] = df["date_occ"].dt.month
        df["day_of_week"] = df["date_occ"].dt.day_name()

    # Convert LAPD TIME OCC format into hour
    if "time_occ" in df.columns:
        df["time_occ"] = df["time_occ"].astype(str).str.zfill(4)
        df["hour"] = df["time_occ"].str[:2].astype(int)

    # Weekend flag
    if "day_of_week" in df.columns:
        df["is_weekend"] = df["day_of_week"].isin(["Saturday", "Sunday"]).astype(int)

    # Keep useful columns only
    useful_columns = [
        "dr_no",
        "date_rptd",
        "date_occ",
        "time_occ",
        "hour",
        "day_of_week",
        "month",
        "year",
        "is_weekend",
        "area_name",
        "crm_cd_desc",
        "vict_age",
        "vict_sex",
        "weapon_desc",
        "status_desc",
        "lat",
        "lon"
    ]

    existing_columns = [col for col in useful_columns if col in df.columns]
    df = df[existing_columns]

    return df


def save_cleaned_data(df, path=PROCESSED_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)


if __name__ == "__main__":
    df_raw = load_data()   # loads full dataset
    df_clean = clean_crime_data(df_raw)
    save_cleaned_data(df_clean)

    print("Cleaning complete.")
    print("Rows:", df_clean.shape[0])
    print("Columns:", df_clean.shape[1])