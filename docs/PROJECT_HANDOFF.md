# Vision-Based Spacecraft Docking --- Project Handoff / Context

## 1. Purpose of this document

This file is a handoff document for starting a new ChatGPT conversation
without losing the important project context.

The project is a ROS 2 Foxy simulation of **vision-based spacecraft
docking**. The system uses a synthetic camera image, target detection, a
proportional controller, and a simulated spacecraft state. The current
goal is to finish the core closed-loop system first, then perform
systematic controller experiments and evaluation.

------------------------------------------------------------------------

# 2. Recommended prompt for a new ChatGPT chat

Copy the prompt below into the new chat:

> I am continuing a project called **vision-based-spacecraft-docking**.
> Please use the attached `PROJECT_HANDOFF.md` as the main project
> context.
>
> The project is a ROS 2 Foxy Python simulation of vision-based
> spacecraft docking. It has a synthetic target/image publisher,
> image/target detector, P controller, simulated spacecraft state,
> `/camera/image_raw`, and `/cmd_vel`.
>
> Current architecture:
>
> ``` text
> Synthetic spacecraft state
>         ↓
> image_publisher
>         ↓
> /camera/image_raw
>         ↓
> image_detector
>         ↓
> target_detector
>         ↓
> image-space + depth error
>         ↓
> P controller
>         ↓
> /cmd_vel
>         ↓
> image_publisher
>         ↓
> spacecraft state update
> ```
>
> Important current facts: - ROS 2 Foxy - Python 3.8 - Control/update
> timestep: `dt = 0.1 s` (10 Hz) - Target position:
> `(x_target, y_target, z_target) = (0, 0, 1)` - Publisher ground-truth
> docking tolerance: x/y = 1.0, z = 0.05 - Detector image-space
> tolerance: x/y = 5 pixels, z = 0.05 - Current controller under
> investigation: P controller - Preliminary `Kp = 0.1` results show
> stable convergence with no obvious oscillation.
>
> The immediate priority is NOT to run more experiments yet. First
> verify that the code has been cleaned up: 1. Initial state must be
> defined once and used both for `SpacecraftState` and
> `experiment_summary.csv`. 2. Docking conditions should use `<=` rather
> than `<`. 3. Detector should stop processing after detector-side
> docking success. 4. Detector should command zero velocity if target
> detection fails, rather than retaining an old command. 5. Publisher
> should stop its command/state loop after ground-truth docking success
> and record the experiment summary. 6. Make sure the CSV output is
> reliable for both successful and, later, failed experiments.
>
> After the code is verified, continue the project by milestones. Do not
> immediately redo all experiments. The next major experimental
> milestone is systematic controller evaluation (different Kp values,
> multiple initial conditions, repeated trials, docking time, success
> rate, final error, and oscillation/overshoot).
>
> Please help me reason about the project as a robotics/control-system
> project, distinguish detector-side success from publisher/ground-truth
> success, and avoid mixing those two concepts.
>
> When suggesting code changes, preserve the existing ROS 2 architecture
> unless there is a clear reason to change it.

------------------------------------------------------------------------

# 3. Project overview

## Project name

`vision-based-spacecraft-docking`

The repository is under:

``` text
~/space_robotics/vision-based-spacecraft-docking/
```

Important directories/files seen during development:

``` text
vision-based-spacecraft-docking/
├── docs/
├── experiments/
│   ├── controller.py
│   ├── docking_position.csv
│   ├── experiment_summary.csv
│   ├── plot_trajectory.py
│   └── ...
├── ros2_ws/
│   ├── src/
│   │   └── docking_vision/
│   │       ├── docking_vision/
│   │       │   ├── controller.py
│   │       │   ├── image_detector.py
│   │       │   ├── image_publisher.py
│   │       │   ├── synthetic_target.py
│   │       │   └── target_detector.py
│   │       ├── package.xml
│   │       ├── setup.py
│   │       └── ...
│   └── ...
└── simulation/
```

------------------------------------------------------------------------

# 4. Software/environment

Known environment from terminal/screenshots:

-   Ubuntu desktop environment
-   ROS 2 Foxy
-   Python 3.8
-   `rclpy`
-   OpenCV
-   `cv_bridge`
-   NumPy
-   Pandas
-   Matplotlib
-   `geometry_msgs.msg.Twist`
-   `sensor_msgs.msg.Image`

The package is named:

``` text
docking_vision
```

Console scripts include:

``` text
image_publisher
image_detector
```

------------------------------------------------------------------------

# 5. Current system architecture

## Node 1 --- Image Publisher / spacecraft simulation

File:

``` text
ros2_ws/src/docking_vision/docking_vision/image_publisher.py
```

Responsibilities:

1.  Maintain simulated spacecraft state `(x,y,z)`.
2.  Receive velocity commands from `/cmd_vel`.
3.  Integrate the state using:

``` python
state.x += command_x * dt
state.y += command_y * dt
state.z += command_z * dt
```

with:

``` python
dt = 0.1
```

4.  Generate a synthetic target image using `create_target()`.
5.  Publish the image on:

``` text
/camera/image_raw
```

6.  Calculate ground-truth state error.
7.  Check ground-truth docking condition.
8.  Save trajectory data to CSV.
9.  Save experiment summary.

------------------------------------------------------------------------

# 6. Current image publisher state model

The target is:

``` python
x_target = 0
y_target = 0
z_target = 1
```

Example initial states used:

``` text
(80, 50, 2)
(-80, -50, 2)
(50, -30, 0.5)
(-100, 70, 1.5)
```

The initial state must be defined only once, e.g.:

``` python
self.initial_x = 80.0
self.initial_y = 50.0
self.initial_z = 2.0

self.state = SpacecraftState(
    self.initial_x,
    self.initial_y,
    self.initial_z
)
```

This fixes an earlier bug where the summary always reported
`(-80,-50,2)` even when a different initial state was actually used.

------------------------------------------------------------------------

# 7. Ground-truth docking condition

Current intended publisher tolerance:

``` python
self.tolerance_x = 1.0
self.tolerance_y = 1.0
self.tolerance_z = 0.05
```

Recommended condition:

``` python
docked = (
    abs(error_x) <= self.tolerance_x
    and abs(error_y) <= self.tolerance_y
    and abs(error_z) <= self.tolerance_z
)
```

This is the simulation's ground-truth docking criterion.

------------------------------------------------------------------------

# 8. Image detector node

File:

``` text
ros2_ws/src/docking_vision/docking_vision/image_detector.py
```

Responsibilities:

1.  Subscribe to `/camera/image_raw`.
2.  Convert ROS Image to OpenCV mono8 using `CvBridge`.
3.  Detect the target using:

``` python
detect_target(cv_image)
```

4.  Calculate image/depth errors.
5.  Call the controller.
6.  Publish velocity commands to:

``` text
/cmd_vel
```

7.  Detect detector-side docking success.
8.  Set command to zero and stop processing after success.

------------------------------------------------------------------------

# 9. Detector error definition

Current image center:

``` text
320, 240
```

Detector gets:

``` python
cx, cy, z = result
```

Then:

``` python
error_x = cx - 320
error_y = cy - 240
error_z = z - 1.0
```

Detector tolerances:

``` python
tolerance_x = 5.0  # pixels
tolerance_y = 5.0  # pixels
tolerance_z = 0.05
```

Recommended condition:

``` python
docked = (
    abs(error_x) <= tolerance_x
    and abs(error_y) <= tolerance_y
    and abs(error_z) <= tolerance_z
)
```

On detector-side success:

``` python
self.command_x = 0.0
self.command_y = 0.0
self.command_z = 0.0
self.docking_success = True
```

and at the start of `image_callback()`:

``` python
if self.docking_success:
    return
```

This prevents repeated:

``` text
SPACE DOCKING SUCCESS
SPACE DOCKING SUCCESS
...
```

after the detector has already succeeded.

------------------------------------------------------------------------

# 10. Important safety behavior

If `detect_target()` returns `None`, the detector should NOT keep
publishing the previous velocity command.

Recommended:

``` python
if result is None:
    print("Target Not Found")

    self.command_x = 0.0
    self.command_y = 0.0
    self.command_z = 0.0

    cv2.waitKey(1)
    return
```

This is a safer behavior for a vision-based control loop.

------------------------------------------------------------------------

# 11. Controller

File:

``` text
ros2_ws/src/docking_vision/docking_vision/controller.py
```

The controller is currently a proportional controller.

Conceptually:

``` text
u = Kp * error
```

The exact axis/sign mapping is defined in the current `controller.py`.

The main Kp under preliminary testing is:

``` text
Kp = 0.1
```

Earlier values tested/investigated include approximately:

``` text
Kp = 0.01
Kp = 0.05
Kp = 0.1
```

Further tuning is planned but should be done systematically later.

------------------------------------------------------------------------

# 12. Important distinction: two docking success signals

There are intentionally two notions of success.

## Detector-side success

Based on what the camera/vision system estimates:

``` text
image target center + estimated z
        ↓
detector error
        ↓
within detector tolerance
        ↓
SPACE DOCKING SUCCESS
```

This represents what the vision/control system believes.

## Publisher/ground-truth success

Based on the simulated spacecraft state:

``` text
actual simulated x,y,z
        ↓
ground-truth state error
        ↓
within ground-truth tolerance
        ↓
DOCKING SUCCESS
```

This is the value used to validate the simulation and write the
experiment summary.

For experiments, the publisher ground-truth result is the more important
final validation signal.

------------------------------------------------------------------------

# 13. Previous issue with Ctrl+C

Earlier, the detector could print:

``` text
SPACE DOCKING SUCCESS
```

and still receive more images because the publisher kept publishing.

The publisher could also continue sending commands until its own
ground-truth docking criterion was reached.

This caused confusion about whether Ctrl+C was pressed too early.

The intended behavior after cleanup is:

``` text
detector success
    ↓
detector command = 0
    ↓
publisher continues only long enough to verify ground truth
    ↓
publisher ground-truth DOCKING SUCCESS
    ↓
CSV summary written
    ↓
Ctrl+C can safely terminate the ROS process
```

The experiment should not be considered complete merely because the
detector prints success; ground-truth success should also be checked
when validating the simulation.

------------------------------------------------------------------------

# 14. Preliminary Kp = 0.1 results

These are preliminary validation results, not yet the final statistical
experiment.

## Initial condition: `(80, 50, 2)` --- first run

Result:

``` text
Docking condition was not reached.
```

The trajectory was very close to the docking region but missed the y
tolerance by a small amount.

Approximate final state from the uploaded trajectory:

``` text
x ≈ 0.73
y ≈ 1.08
z ≈ 1.0165
```

With ground-truth tolerance:

``` text
|x| <= 1
|y| <= 1
|z-1| <= 0.05
```

only y was slightly outside.

This was not divergence or oscillation.

------------------------------------------------------------------------

## Initial condition: `(80, 50, 2)` --- V2

Result:

``` text
Docking state:
0.57 0.99 1.014188...
Time to dock: 42.3 seconds
```

This run successfully reached the tolerance.

------------------------------------------------------------------------

## Initial condition: `(-80, -50, 2)`

Result:

``` text
Docking state:
-0.99 -0.72 1.033857...
Time to dock: 38.7 seconds
```

Successful.

------------------------------------------------------------------------

## Initial condition: `(50, -30, 0.5)`

Result:

``` text
Docking state:
0.97 0.72 1.017574...
Time to dock: 36.4 seconds
```

Successful.

------------------------------------------------------------------------

## Initial condition: `(-100, 70, 1.5)`

Result:

``` text
Docking state:
0.40 1.00 1.019837...
Time to dock: 43.0 seconds
```

Successful / at the y tolerance boundary.

------------------------------------------------------------------------

# 15. Preliminary interpretation of Kp = 0.1

Observed behavior:

-   Stable convergence.
-   No obvious oscillation in the trajectory plots.
-   Error decreases approximately monotonically.
-   State trajectories resemble exponential-like convergence.
-   Docking time in preliminary successful runs is roughly 36--43
    seconds.
-   The initial `(80,50,2)` condition produced one near-miss followed by
    a successful V2 run.
-   This is not enough data to claim a statistically reliable success
    rate.

Important interpretation:

**Do not define "good Kp" as a Kp that produces oscillation.**

The desired progression for controller tuning is conceptually:

``` text
Kp too low
    ↓
stable but slow

Kp appropriate
    ↓
stable + reasonably fast convergence

Kp too high
    ↓
overshoot / oscillation / possible instability
```

------------------------------------------------------------------------

# 16. Trajectory CSV

The publisher writes:

``` text
docking_position.csv
```

Columns:

``` text
time
x
y
z
error_x
error_y
error_z
```

This is used by:

``` text
experiments/plot_trajectory.py
```

The plots currently show:

1.  Spacecraft State
2.  Docking Error

The plots for Kp=0.1 show smooth convergence without obvious
oscillation.

------------------------------------------------------------------------

# 17. Experiment summary CSV

Current intended columns:

``` text
initial_x
initial_y
initial_z
time_to_dock
final_x
final_y
final_z
success
```

Important bug already identified:

The initial values were previously hard-coded as:

``` python
self.initial_x = -80
self.initial_y = -50
self.initial_z = 2
```

while the actual `SpacecraftState` was changed for other experiments.

This caused incorrect metadata in `experiment_summary.csv`.

The fix is to use:

``` python
self.state = SpacecraftState(
    self.initial_x,
    self.initial_y,
    self.initial_z
)
```

and use the same `self.initial_*` fields when writing the summary.

------------------------------------------------------------------------

# 18. Experiment plan for a later milestone

Do NOT spend time running this immediately. The current priority is
system cleanup and milestone progression.

When the experiment milestone begins:

## Kp values

At minimum:

``` text
0.01
0.05
0.10
0.20
```

Potentially add more values if needed.

## Initial conditions

Use:

``` text
(80, 50, 2)
(-80, -50, 2)
(50, -30, 0.5)
(-100, 70, 1.5)
```

## Repetitions

Prefer:

``` text
3–5 trials per Kp × initial condition
```

if runtime permits.

## Metrics

Collect:

-   Success/failure
-   Docking time
-   Final x error
-   Final y error
-   Final z error
-   Maximum absolute error / overshoot if useful
-   Oscillation behavior
-   Mean docking time
-   Standard deviation
-   Success rate

The final experiment should answer:

> Which Kp gives the best compromise between docking speed, stability,
> accuracy, and robustness across different initial conditions?

------------------------------------------------------------------------

# 19. Future improvement: record failed experiments

Current summary writing is mainly success-oriented.

For future experimental work, make sure a failed run also records:

``` text
initial state
elapsed time
final state
final errors
success = False
```

This is important because a failed run is still useful data.

For example:

``` text
initial_x,initial_y,initial_z,time_to_dock,final_x,final_y,final_z,success
80,50,2,42.1,0.73,1.08,1.0165,False
```

This allows failure rate and robustness to be analyzed properly.

------------------------------------------------------------------------

# 20. Milestone status

## Milestone 1 --- Basic system

Status: **Essentially complete**

Completed:

-   Synthetic target
-   Simulated spacecraft state
-   Image publisher
-   Camera topic
-   Target detection
-   Image/depth error calculation
-   P controller
-   `/cmd_vel`
-   Closed-loop simulation

------------------------------------------------------------------------

## Milestone 2 --- Controller + docking logic

Status: **Nearly complete**

Completed / demonstrated:

-   P controller
-   x/y/z control
-   Docking tolerance
-   Docking success condition
-   Detector-side command stop
-   Publisher-side ground-truth success
-   Preliminary Kp=0.1 validation

Remaining cleanup:

-   Stop detector processing after success
-   Stop/zero commands after target loss
-   Consistent initial-state configuration
-   Correct CSV metadata
-   Better failed-experiment logging
-   Parameterize Kp and initial conditions cleanly

------------------------------------------------------------------------

## Milestone 3 --- Experimental framework

Status: **Not started systematically**

Planned:

-   Multiple Kp values
-   Multiple initial conditions
-   Repeated trials
-   Mean/std docking time
-   Success rate
-   Final errors
-   Oscillation/overshoot analysis
-   Comparison plots/tables

This milestone DOES require experiment data.

------------------------------------------------------------------------

## Milestone 4 --- Controller evaluation

Status: **Future**

Goal:

Select/justify a suitable Kp based on:

``` text
speed
accuracy
stability
robustness
```

rather than selecting it from a single trajectory.

------------------------------------------------------------------------

# 21. What to do next

Do NOT immediately rerun all experiments.

First:

1.  Verify `image_publisher.py` initial-state handling.
2.  Verify `image_detector.py` stops after detector success.
3.  Verify lost-target behavior sets command to zero.
4.  Verify publisher stops after ground-truth success.
5.  Verify the correct initial state appears in
    `experiment_summary.csv`.
6.  Run one short end-to-end sanity test.
7.  Inspect CSV output.
8.  Then move to the next project milestone.

After that, experiment work can be resumed on another day.

------------------------------------------------------------------------

# 22. Important engineering interpretation

The project is not just about making the graph reach zero.

The intended control loop is:

``` text
Vision
  ↓
Perception
  ↓
State/error estimation
  ↓
Controller
  ↓
Command
  ↓
Spacecraft dynamics
  ↓
New image
  ↓
Vision
```

The important research/engineering question is whether this closed-loop
system can robustly converge to the docking target under different
initial conditions and controller gains.

The simulation currently provides two useful perspectives:

-   **Estimated/vision state** --- what the controller sees.
-   **Ground-truth state** --- what the simulated spacecraft actually
    does.

Keeping these separate is important for later evaluation.

------------------------------------------------------------------------

# 23. Current conclusion

At the current point in the project:

**Kp = 0.1 is a promising preliminary value.**

The observed trajectories are stable and non-oscillatory, with
successful docking from several different initial conditions. However,
there is not yet enough repeated experimental data to make a
statistically strong claim about the best Kp.

The next immediate task is code cleanup and system verification, not
more controller tuning.

Once the system is clean and reproducible, the experimental milestone
can systematically compare Kp values.

------------------------------------------------------------------------

# 24. Key files to ask about first in a new chat

If the new ChatGPT needs to inspect the implementation, ask it to review
these files first:

``` text
ros2_ws/src/docking_vision/docking_vision/controller.py
ros2_ws/src/docking_vision/docking_vision/image_detector.py
ros2_ws/src/docking_vision/docking_vision/image_publisher.py
ros2_ws/src/docking_vision/docking_vision/target_detector.py
ros2_ws/src/docking_vision/docking_vision/synthetic_target.py
experiments/plot_trajectory.py
```

The most important three are:

``` text
controller.py
image_detector.py
image_publisher.py
```

------------------------------------------------------------------------

# 25. Communication preference for future work

When continuing this project:

-   Explain why a change is needed before changing architecture.
-   Prefer minimal, targeted code changes.
-   Distinguish simulation ground truth from vision estimates.
-   Do not assume an experiment is successful solely from detector
    output.
-   Use actual CSV results when making quantitative claims.
-   Avoid re-running experiments unnecessarily.
-   Keep milestone progress explicit.
-   When an experiment is needed, define exactly what variables and
    metrics should be collected first.
