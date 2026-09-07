# Vision-Based Spacecraft Docking — Project Summary

## 1. Project Overview

**Project:** `vision-based-spacecraft-docking`

**Goal:** Develop a practical ROS 2-based autonomous spacecraft docking MVP using computer vision, relative-state estimation, control, simulation, experiment logging, and quantitative evaluation.

The project is designed to build practical skills relevant to space robotics engineering and robot software engineering.

The project is intentionally divided into an MVP stage and a later research-grade extension stage.

## 2. MVP Scope

The current MVP focuses on demonstrating a complete closed-loop docking pipeline rather than realistic spacecraft physics.

```text
Camera
  ↓
Target Detection
  ↓
Relative State / Error Estimation
  ↓
Proportional Controller
  ↓
Command
  ↓
Simulated Spacecraft Motion
  ↓
Updated Camera Image
  ↓
Target Detection
  ↓
...
```

The main engineering goal was to make this loop work end-to-end and produce reproducible experimental data.

## 3. ROS 2 Implementation

The project uses the ROS 2 workspace:

```text
~/space_robotics/vision-based-spacecraft-docking/ros2_ws
```

Main ROS 2 nodes:

- `/image_detector_node`
- `/image_publisher_node`

Main topics include:

```text
/camera/image_raw
/cmd_vel
```

The detector processes the camera image, estimates target state/error, and generates control commands. The publisher/simulation node generates synthetic images and updates the simulated spacecraft state.

## 4. Vision and State Estimation MVP

The current target is synthetic and detected using simplified image processing.

The detector obtains:

```text
cx
cy
z
```

and computes:

```text
error_x = cx - 320
error_y = cy - 240
error_z = z - 1.0
```

The current docking target is:

```text
x = 0
y = 0
z = 1
```

This is intentionally a simplified perception/state-estimation model for the MVP.

## 5. Controller

The MVP uses a proportional controller with:

```text
Kp = 0.2
```

The controller uses estimated errors to generate commands that drive the simulated state toward the docking target.

The gain is configurable through ROS 2 parameters and YAML.

The detector parameter was verified using ROS 2 parameter commands.

The publisher also stores the same `kp` value for experiment logging; it is not the source of the controller gain.

## 6. Configuration

Configuration is stored in:

```text
src/docking_vision/config/controller.yaml
```

Important parameters include:

```text
kp: 0.2
initial_x: -100.0
initial_y: 100.0
initial_z: 1.5
trial_id: 1
dt: 0.1
target_x: 0.0
target_y: 0.0
target_z: 1.0
tolerance_x: 1.0
tolerance_y: 1.0
tolerance_z: 0.05
```

## 7. Safety and Control Logic

The detector was updated to handle target-detection failure safely.

When detection returns `None`, the system:

- Prints `Target Not Found`
- Sends zero commands
- Processes the OpenCV event loop
- Returns from the callback

When docking is reached:

- Commands are set to zero
- Docking success is recorded
- Further motion is stopped

## 8. Experiment Logging

Trajectory data is recorded in:

```text
docking_position.csv
```

Schema:

```text
run_id, trial_id, kp, time, x, y, z, error_x, error_y, error_z
```

Experiment-level results are stored in:

```text
experiment_summary.csv
```

and the controlled dataset used for final analysis is:

```text
experiment_summary_controlled.csv
```

Schema:

```text
run_id, trial_id, kp, initial_x, initial_y, initial_z,
time_to_dock, final_x, final_y, final_z, success
```

The logging system appends to existing CSV files rather than overwriting previous experiments. Each run receives a timestamp-based `run_id`.

## 9. Controlled Test Cases

Three controlled experiments were completed.

| Trial | Initial X | Initial Y | Initial Z | Kp |
|---|---:|---:|---:|---:|
| TC1 | 80 | 50 | 2.0 | 0.2 |
| TC2 | -100 | -100 | 1.5 | 0.2 |
| TC3 | 50 | -30 | 0.5 | 0.2 |

These were scenario tests, not controller-gain tuning experiments.

## 10. Experimental Results

All three controlled trials successfully reached the defined docking condition.

### Overall

```text
Total runs: 3
Successful runs: 3
Success rate: 100.0%
Average time to dock: 18.233 s
Average final position error: 1.215
Average initial position error: 98.026
```

### Per Trial

| Trial | Initial Position Error | Time to Dock | Final Position Error | Success |
|---|---:|---:|---:|---|
| TC1 | 94.345 | 20.0 s | 1.139 | True |
| TC2 | 141.422 | 17.8 s | 1.330 | True |
| TC3 | 58.312 | 16.9 s | 1.177 | True |

The exact physical units of these position-error values should not be assumed until the simulation state units are explicitly defined.

## 11. Result Interpretation

- **Largest initial error:** TC2 = `141.422`
- **Shortest docking time:** TC3 = `16.9 s`
- **Smallest final error:** TC1 = `1.139`

For these three trials, a larger initial position error did not consistently result in a longer docking time. TC2 started farther from the target than TC1 but completed docking faster.

This should not be generalized into a claim that initial error has no effect because only three trials were evaluated.

The position error magnitude decreased over time in all three trials, indicating that the proportional controller drove the simulated spacecraft state toward the docking target in the simplified model.

## 12. Visualization

The final MVP visualization consists of:

1. X-Y trajectory
2. X position vs. time
3. Y position vs. time
4. Z position vs. time
5. Position error magnitude vs. time

The plots are generated from:

```text
docking_position.csv
```

Trajectory/time-series visualization is kept separate from experiment-level metric analysis.

## 13. Analysis Script

Experiment-level analysis is implemented in:

```text
analyze_results.py
```

It calculates:

- Final position error
- Initial position error
- Success rate
- Average time to dock
- Average final position error
- Average initial position error
- Results grouped by trial

Initial position error:

```text
sqrt(
    initial_x² +
    initial_y² +
    (initial_z - target_z)²
)
```

with:

```text
target = (0, 0, 1)
```

## 14. Phase 7 Progress

Phase 7 covered:

- 7.1 Metrics
- 7.2 Test Cases
- 7.3 Experimental Protocol
- 7.4 Controlled Runs
- 7.5 Analysis
- 7.6 Visualization
- 7.7 Interpretation
- 7.8 Discussion & Limitations

At this point, Phase 7 is complete.

## 15. Overall Project Status

```text
Setup                    COMPLETE
ROS 2                    COMPLETE
Vision MVP               COMPLETE
Controller MVP           COMPLETE
Simulation MVP           COMPLETE
Experiment Logging       COMPLETE
Controlled Tests         COMPLETE
Metrics                  COMPLETE
Visualization            COMPLETE
Interpretation           COMPLETE
Discussion & Limitations COMPLETE
Phase 7                  COMPLETE
```

## 16. Research-Grade Features Deferred

The following are intentionally not part of the current MVP:

- Realistic 6-DoF spacecraft dynamics
- Orbital mechanics
- Real camera hardware
- Robust real-world perception
- 6-DoF pose estimation / PnP
- Kalman/EKF state estimation
- Sensor noise and latency modeling
- Disturbance modeling
- Controller tuning across multiple Kp values
- Large-scale statistical validation
- Monte Carlo robustness analysis

These can form a later research-grade roadmap.

## 17. Next Phase

The next phase should focus on final integration and packaging before adding research-grade complexity.

Likely tasks:

1. Clean up code and repository structure
2. Update the README
3. Document build/run instructions
4. Document experiment reproduction
5. Organize experiment outputs
6. Review final plots and results
7. Prepare a final MVP demonstration
8. Clearly separate completed MVP work from future research work
9. Commit/tag the completed MVP milestone

The current repository README still describes the project as being in initial setup, so updating it is an important final packaging task.
