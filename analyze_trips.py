import pandas as pd
import datetime

def analyze_trips(filepath):
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return

    print(f"Analysis of {filepath}")
    print("-" * 30)

    # Number of trips
    num_trips = len(df)
    print(f"Total number of trips: {num_trips}")

    # Temporal coverage
    # timestamps are likely unix timestamps based on sample output
    if 'time_start' in df.columns:
        min_time = df['time_start'].min()
        max_time = df['time_start'].max()

        # Check if reasonable timestamp
        if min_time > 946684800: # Year 2000
            min_date = datetime.datetime.fromtimestamp(min_time)
            max_date = datetime.datetime.fromtimestamp(max_time)

            print(f"Temporal coverage: {min_date} to {max_date}")
            print(f"Duration of coverage: {max_date - min_date}")
        else:
             print("Timestamps do not appear to be standard Unix timestamps.")

    # Duration stats
    if 'duration' in df.columns:
        print(f"Duration (seconds): Mean={df['duration'].mean():.2f}, Median={df['duration'].median():.2f}")

    # Distance stats
    if 'distance' in df.columns:
        print(f"Distance (meters): Mean={df['distance'].mean():.2f}, Median={df['distance'].median():.2f}")

    # Check for waypoints (by proxy of schema knowledge, but here we check columns)
    print("Columns:", df.columns.tolist())
    if 'waypoints' in df.columns:
        print("Waypoints column found.")
    else:
        print("No explicit waypoints column found (only start/end coordinates).")

if __name__ == "__main__":
    analyze_trips("sample/trips.csv")
