import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("docking_position.csv")

plt.plot(df["time"], df["x"], label="x")
plt.plot(df["time"], df["y"], label="y")
plt.plot(df["time"], df["z"], label="z")

plt.xlabel("Time (s)")
plt.ylabel("State")
plt.title("Spacecraft State")
plt.legend()
plt.grid()

plt.show()

plt.figure()

plt.plot(df["time"], df["error_x"], label="error_x")
plt.plot(df["time"], df["error_y"], label="error_y")
plt.plot(df["time"], df["error_z"], label="error_z")

plt.axhline(0, linestyle="--")

plt.xlabel("Time (s)")
plt.ylabel("Error")
plt.title("Docking Error")
plt.legend()
plt.grid()

plt.show()

tolerance_x = 1.0
tolerance_y = 1.0
tolerance_z = 0.05

docked = (
    (df["error_x"].abs() < tolerance_x) &
    (df["error_y"].abs() < tolerance_y) &
    (df["error_z"].abs() < tolerance_z)
)

if docked.any():

    first_dock_index = docked.idxmax()
    dock_time = df.loc[first_dock_index, "time"]

    print("Initial state:")
    print(
        df.iloc[0]["x"],
        df.iloc[0]["y"],
        df.iloc[0]["z"]
    )

    print("Docking state:")
    print(
        df.loc[first_dock_index, "x"],
        df.loc[first_dock_index, "y"],
        df.loc[first_dock_index, "z"]
    )

    print("Time to dock:", dock_time, "seconds")

else:
    print("Docking condition was not reached.")