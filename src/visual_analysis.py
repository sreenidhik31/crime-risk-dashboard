import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


DATA_PATH = "data/processed/crime_cleaned.csv"
VISUAL_PATH = "visuals"


def load_cleaned_data(path=DATA_PATH):
    return pd.read_csv(path, low_memory=False)


def save_crime_type_chart(df):
    os.makedirs(VISUAL_PATH, exist_ok=True)

    top_crimes = df["crm_cd_desc"].value_counts().head(10)

    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_crimes.values, y=top_crimes.index)
    plt.title("Top 10 Crime Types")
    plt.xlabel("Number of Crimes")
    plt.ylabel("Crime Type")
    plt.tight_layout()
    plt.savefig(f"{VISUAL_PATH}/top_crime_types.png")
    plt.close()


def save_monthly_trend_chart(df):
    df["date_occ"] = pd.to_datetime(df["date_occ"], errors="coerce")
    monthly = df.groupby(df["date_occ"].dt.to_period("M")).size()
    monthly.index = monthly.index.astype(str)

    plt.figure(figsize=(12, 6))
    plt.plot(monthly.index, monthly.values)
    plt.title("Monthly Crime Trend")
    plt.xlabel("Month")
    plt.ylabel("Crime Count")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(f"{VISUAL_PATH}/monthly_crime_trend.png")
    plt.close()


def save_hour_day_heatmap(df):
    pivot = df.pivot_table(
        index="day_of_week",
        columns="hour",
        values="crm_cd_desc",
        aggfunc="count",
        fill_value=0
    )

    day_order = [
        "Monday", "Tuesday", "Wednesday", "Thursday",
        "Friday", "Saturday", "Sunday"
    ]

    pivot = pivot.reindex(day_order)

    plt.figure(figsize=(14, 6))
    sns.heatmap(pivot, cmap="Reds")
    plt.title("Crime Frequency by Day and Hour")
    plt.xlabel("Hour of Day")
    plt.ylabel("Day of Week")
    plt.tight_layout()
    plt.savefig(f"{VISUAL_PATH}/day_hour_heatmap.png")
    plt.close()


if __name__ == "__main__":
    df = load_cleaned_data()

    save_crime_type_chart(df)
    save_monthly_trend_chart(df)
    save_hour_day_heatmap(df)

    print("Visuals created successfully.")