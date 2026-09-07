from pathlib import Path
import pandas as pd
import numpy as np


# Get the directory containing this Python script
script_dir = Path(__file__).resolve().parent

# CSV file is in the same directory as this script
csv_path = script_dir / 'experiment_summary_controlled.csv'

# Load CSV
df = pd.read_csv(csv_path)
# df.groupby('trial_id')
# print(df)

#Final Position Error
target = (0, 0, 1)
final_x = df["final_x"]
final_y = df["final_y"]
final_z = df["final_z"]
# print(final_x.loc[0])
# print(final_x.loc[1])
# print(final_x)
# print(final_y)
# print(final_z)
error = np.sqrt(
    (final_x - target[0])**2 +
    (final_y - target[1])**2 +
    (final_z - target[2])**2
)
# print(error)
df["final_position_error"] = error

#initial position error
initial_x = df["initial_x"]
initial_y = df["initial_y"]
initial_z = df["initial_z"]
initial_error = np.sqrt(initial_x **2 +
                        initial_y **2 +
                        (initial_z - target[2]) ** 2)

df["initial_position_error"] = initial_error

#Success Rate
total_runs = len(df)
successful_runs = df['success'].sum()
success_rate = (successful_runs / total_runs) * 100

#Average Time to Dock
successful = df[df['success'] == True]
# print(successful)
average_time_to_dock = successful['time_to_dock'].mean()
# print(average_time_to_dock)

#Average final position error
average_final_position_error = successful["final_position_error"].mean()

#Average initial position error
average_initial_position_error = successful["initial_position_error"].mean()

# Display the first 5 rows
print(df.head())
print("=== Overall Results ===")

print("Total runs: ", total_runs)
print("Successful runs: ", successful_runs)
print("Successful rate: ", success_rate , "%")

print("Average time to dock: ", average_time_to_dock , "s")
print("Average final position error:", average_final_position_error)
print("Average initial position error:",average_initial_position_error)

print("=== Results by Trial ===")

grouped = df.groupby("trial_id")
for trial_id, group in grouped:
    print("Trial : ", trial_id)
    #.iloc[0] = เอาข้อมูลแถวแรกของ DataFrame/Series
    print("Success: ", group["success"].sum())
    print("Time to dock: ", group["time_to_dock"].mean())
    print("initial position error: ", group["initial_position_error"].mean())
    print("Final position error: ", group["final_position_error"].mean())

results = df[[
    "trial_id",
    "initial_position_error",
    "time_to_dock",
    "final_position_error",
    "success"
]]
results = results.round(3)
print(results)