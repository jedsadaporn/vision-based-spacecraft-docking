import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_csv("docking_position.csv")

print(df.groupby(["trial_id", "run_id"]).size())

#Prove CSV have TC1-TC3
# print(df["trial_id"].unique())
print(df.groupby("trial_id").size())

plt.figure()
for trial_id in [1, 2, 3]:
    trial = df[df["trial_id"] == trial_id]

    # trajectory
    # plt.plot(trial["x"], trial["y"], label="Trajectory")
    plt.plot(
    trial["x"],
    trial["y"],
    label=f"TC{trial_id}"
    )

    # start point
    # plt.scatter(
    #     trial.iloc[0]["x"],
    #     trial.iloc[0]["y"],
    #     label=f"TC{trial_id}"
    # )

# docking target
plt.scatter(0, 0, label="Docking Target")
plt.xlabel("X Axis")
plt.ylabel("Y Axis")
plt.title("X-Y trajectory")
plt.legend()
plt.grid()
plt.show()

plt.figure()
for trial_id in [1, 2, 3]:
    trial = df[df["trial_id"] == trial_id]

    plt.plot(
        trial["time"],
        trial["x"],
        label=f"TC{trial_id}"
    )
    # plt.plot(trial["time"], trial["y"], label="y")
    # plt.plot(trial["time"], trial["z"], label="z")

plt.xlabel("Time (s)")
plt.ylabel("X Position")
plt.title("X Position vs Time")
plt.legend()
plt.grid()
plt.show()

plt.figure()
for trial_id in [1, 2, 3]:
    trial = df[df["trial_id"] == trial_id]

    plt.plot(
        trial["time"],
        trial["y"],
        label=f"TC{trial_id}"
    )

plt.xlabel("Time (s)")
plt.ylabel("Y Position")
plt.title("Y Position vs Time")
plt.legend()
plt.grid()
plt.show()

plt.figure()
for trial_id in [1, 2, 3]:
    trial = df[df["trial_id"] == trial_id]

    plt.plot(
        trial["time"],
        trial["z"],
        label=f"TC{trial_id}"
    )

plt.xlabel("Time (s)")
plt.ylabel("Z Position")
plt.title("Z Position vs Time")
plt.legend()
plt.grid()
plt.show()

tolerance_x = 1.0
tolerance_y = 1.0
tolerance_z = 0.05

plt.figure()
for trial_id in [1, 2, 3]:
    trial = df[df["trial_id"] == trial_id]

    # Find Error Magnitude
    error_magnitude = np.sqrt(
        trial["error_x"]**2 +
        trial["error_y"]**2 +
        trial["error_z"]**2
    )

    # plt.plot(trial["time"], trial["error_x"], label="error_x")
    # plt.plot(trial["time"], trial["error_y"], label="error_y")
    # plt.plot(trial["time"], trial["error_z"], label="error_z")

    plt.plot(
        trial["time"],
        error_magnitude,
        label=f"TC{trial_id}"
    )

    docked = (
        (trial["error_x"].abs() < tolerance_x) &
        (trial["error_y"].abs() < tolerance_y) &
        (trial["error_z"].abs() < tolerance_z)
    )

    if docked.any():

        first_dock_index = docked.idxmax()
        dock_time = trial.loc[first_dock_index, "time"]

        print("Initial state:")
        print(
            trial.iloc[0]["x"],
            trial.iloc[0]["y"],
            trial.iloc[0]["z"]
        )

        print("Docking state:")
        print(
            trial.loc[first_dock_index, "x"],
            trial.loc[first_dock_index, "y"],
            trial.loc[first_dock_index, "z"]
        )

        print("Time to dock:", dock_time, "seconds")

    else:
        print("Docking condition was not reached.")


# plt.axhline(0, linestyle="--")

plt.xlabel("Time (s)")
plt.ylabel("Position Error Magnitude")
plt.title("Position Error Magnitude vs Time")
plt.legend()
plt.grid()

plt.show()
