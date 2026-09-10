  # Vision-Based Autonomous Spacecraft Docking

  A project-based learning project for developing practical skills in **Space Robotics** and **Robot Software Engineering** through a simplified vision-based autonomous spacecraft docking system using ROS 2, computer vision, simulation, control, experiment logging, and evaluation.

  The project follows an **engineering-first MVP approach**. The current MVP focuses on building a complete, configurable, testable, and reproducible closed-loop docking pipeline. Research-grade capabilities such as 6-DoF pose estimation, state estimation, spacecraft dynamics, and advanced GNC are intentionally left as future extensions.

  ---

  ## Project Goal

  Build an end-to-end ROS 2 vision-based spacecraft docking prototype that demonstrates the engineering workflow of:

  1. Capturing or generating camera images
  2. Detecting a docking target
  3. Estimating relative target position
  4. Computing position error
  5. Applying a proportional visual servoing controller
  6. Commanding simulated spacecraft motion
  7. Detecting the docking condition
  8. Logging trajectories and experiment results
  9. Evaluating the controller through controlled experiments

  The goal is not to build a flight-ready spacecraft docking system, but to develop practical engineering skills that can later be extended toward research-grade space robotics systems.

  ---

  ## Current Status

  ### 🟢 MVP Complete

  The core closed-loop docking system and initial experimental evaluation are complete.

  | Component | Status |
  |---|---|
  | ROS 2 node architecture | ✅ |
  | Camera / image pipeline | ✅ |
  | Synthetic target generation | ✅ |
  | Target detection | ✅ |
  | Relative position estimation | ✅ |
  | Position error calculation | ✅ |
  | Proportional controller | ✅ |
  | Closed-loop spacecraft motion | ✅ |
  | Docking condition detection | ✅ |
  | Safety / failure handling | ✅ |
  | ROS 2 parameter configuration | ✅ |
  | Experiment logging | ✅ |
  | Controlled test cases | ✅ |
  | Result analysis | ✅ |
  | Trajectory visualization | ✅ |
  | Discussion and limitations | ✅ |
  | MVP documentation | ✅ |
  | Gazebo / high-fidelity simulation | ⏳ Future |
  | Research-grade extensions | ⏳ Future |

  ---

  ## MVP System Architecture

  The current MVP implements the following closed-loop pipeline:

  ```text
  Camera / Synthetic Image
            ↓
      Target Detection
            ↓
  Relative Position Estimation
            ↓
      Position Error
            ↓
  Proportional Controller
            ↓
        /cmd_vel
            ↓
  Simulated Spacecraft Motion
            ↓
      Docking Condition
            ↓
  Experiment Logging
            ↓
        Evaluation
  ```

  The system is implemented as ROS 2 nodes communicating through ROS 2 topics and configurable through ROS 2 parameters.

  ---

  ## MVP Pipeline

  ```text
  Image Publisher
        ↓
  /camera/image_raw
        ↓
  Image Detector
        ↓
  Target Position
        ↓
  Position Error
        ↓
  P Controller
        ↓
  /cmd_vel
        ↓
  Image Publisher
        ↓
  Updated Spacecraft State
        ↓
  Docking Check
  ```

  The current controller uses proportional control:

  ```text
  command = -Kp × error
  ```

  where the position error is calculated relative to the docking target.

  ---

  ## ROS 2 Nodes

  ### `image_publisher_node`

  Responsible for:

  - Generating the synthetic camera image
  - Maintaining the simulated spacecraft state
  - Receiving velocity commands
  - Updating spacecraft position
  - Checking the docking condition
  - Logging trajectory data
  - Recording experiment summaries

  ### `image_detector_node`

  Responsible for:

  - Receiving camera images
  - Detecting the synthetic docking target
  - Estimating target position
  - Computing relative position error
  - Generating proportional control commands
  - Handling target-loss and docking-success conditions

  ---

  ## Engineering Skills Demonstrated

  ### ROS 2

  - Node architecture
  - Topics and message communication
  - Parameters
  - ROS 2 command-line tools
  - Package structure
  - Runtime configuration

  ### Robot Software Engineering

  - Modular node design
  - Configuration through YAML
  - Logging
  - CSV experiment recording
  - Failure handling
  - Debugging
  - Reproducible experiment setup
  - Repository organization

  ### Computer Vision

  - Image generation
  - Binary image processing
  - Target detection
  - Contour / bounding-box based localization
  - Image-coordinate reasoning

  ### Robotics / Control

  - Relative position representation
  - Position error calculation
  - Visual servoing
  - Proportional control
  - Closed-loop motion
  - Docking tolerance checking

  ### Experimental Engineering

  - Defined test cases
  - Controlled runs
  - Time-to-dock measurement
  - Final position error
  - Success rate
  - Trajectory logging
  - Automated result analysis
  - Visualization
  - Discussion of limitations

  ---

  ## Experiment and Evaluation

  The MVP includes controlled docking experiments using a fixed proportional gain:

  ```text
  Kp = 0.2
  ```

  Three controlled test cases were used for the Phase 7 evaluation.

  | Test Case | Initial State | Time to Dock | Success |
  |---|---|---:|---|
  | TC1 | (80, 50, 2.0) | 20.0 s | ✅ |
  | TC2 | (-100, -100, 1.5) | 17.8 s | ✅ |
  | TC3 | (50, -30, 0.5) | 16.9 s | ✅ |

  ### Controlled Evaluation Summary

  ```text
  Total runs:             3
  Successful runs:       3
  Success rate:         100%
  Average time to dock: 18.23 s
  ```

  The evaluation demonstrates that the MVP controller successfully drives all three tested initial conditions toward the defined docking condition.

  These results are intended as **engineering validation of the MVP**, not as statistical validation of a flight-ready docking algorithm.

  ---

  ## Experiment Data

  Current experiment outputs are organized under:

  ```text
  experiments/
  ├── experiment_summary_controlled.csv
  │
  ├── experiment_result/
  │   ├── docking_position.csv
  │   ├── experiment_summary.csv
  │   │
  │   └── historical/
  │       ├── docking_position_history.csv
  │       └── experiment_summary_history.csv
  │
  └── debug_images/
  ```

  Historical experiment data is retained separately to preserve development and experiment traceability.

  ---

  ## Repository Structure

  ```text
  vision-based-spacecraft-docking/
  │
  ├── docs/
  │   ├── 7.8_discussion_and_limitations.md
  │   ├── experiment_note.md
  │   ├── project_summary_phase_1_to_7.md
  │   └── PROJECT_HANDOFF.md
  │
  ├── experiments/
  │   ├── analyze_results.py
  │   ├── controller.py
  │   ├── plot_trajectory.py
  │   ├── synthetic_target.py
  │   ├── target_detector.py
  │   ├── experiment_summary_controlled.csv
  │   │
  │   ├── debug_images/
  │   │
  │   └── experiment_result/
  │       ├── docking_position.csv
  │       ├── experiment_summary.csv
  │       └── historical/
  │
  ├── ros2_ws/
  │   └── src/
  │       └── docking_vision/
  │           ├── config/
  │           │   └── controller.yaml
  │           └── docking_vision/
  │               ├── image_detector.py
  │               └── image_publisher.py
  │
  ├── simulation/
  │   └── .gitkeep
  │
  ├── tests/
  │   └── .gitkeep
  │
  ├── .gitignore
  └── README.md
  ```

  ---

  ## How to Run

  ### 1. Enter the ROS 2 workspace

  ```bash
  cd ~/space_robotics/vision-based-spacecraft-docking/ros2_ws
  ```

  ### 2. Build the package

  ```bash
  colcon build
  ```

  ### 3. Source the workspace

  ```bash
  source install/setup.bash
  ```

  ### 4. Run the image publisher

  ```bash
  ros2 run docking_vision image_publisher \
    --ros-args \
    --params-file src/docking_vision/config/controller.yaml
  ```

  ### 5. Run the image detector

  In another terminal:

  ```bash
  cd ~/space_robotics/vision-based-spacecraft-docking/ros2_ws
  source install/setup.bash

  ros2 run docking_vision image_detector \
    --ros-args \
    --params-file src/docking_vision/config/controller.yaml
  ```

  The two nodes communicate through the ROS 2 image and velocity-command topics.

  ---

  ## Configuration

  Controller and experiment parameters are configured through:

  ```text
  ros2_ws/src/docking_vision/config/controller.yaml
  ```

  Example:

  ```yaml
  image_detector_node:
    ros__parameters:
      kp: 0.2

  image_publisher_node:
    ros__parameters:
      kp: 0.2
      initial_x: 50.0
      initial_y: -30.0
      initial_z: 0.5
      trial_id: 4
      dt: 0.1
      target_x: 0.0
      target_y: 0.0
      target_z: 1.0
      tolerance_x: 1.0
      tolerance_y: 1.0
      tolerance_z: 0.05
  ```

  Parameters allow different initial conditions and controller configurations to be tested without modifying the source code.

  ---

  ## Analysis

  Experimental results can be analyzed using:

  ```bash
  python3 experiments/analyze_results.py
  ```

  Trajectory data can be visualized using:

  ```bash
  python3 experiments/plot_trajectory.py
  ```

  The experiment workflow is:

  ```text
  Run Experiment
        ↓
  Record Trajectory
        ↓
  Record Summary
        ↓
  Analyze Results
        ↓
  Visualize Trajectory
        ↓
  Interpret Results
  ```

  ---

  ## Limitations

  The current MVP intentionally uses a simplified simulation and perception model.

  ### Current limitations

  - Simplified spacecraft motion model
  - Synthetic camera images
  - Simplified target detection
  - Relative position rather than full 6-DoF pose estimation
  - Fixed proportional controller gain
  - Limited number of controlled experimental trials
  - Simplified state representation
  - Simplified docking dynamics
  - No realistic camera calibration model
  - No measurement noise or communication latency model
  - No spacecraft attitude dynamics
  - No orbital dynamics

  Therefore, the current system should be considered an **engineering learning and validation prototype**, not a flight-ready autonomous docking system.

  ---

  ## Future Research Extensions

  The following capabilities are intentionally outside the current MVP scope.

  ### Perception and Pose Estimation

  - Camera calibration
  - Feature / marker-based detection
  - PnP-based 6-DoF pose estimation
  - More realistic spacecraft visual models

  ### State Estimation

  - Kalman filtering
  - Extended Kalman Filter (EKF)
  - Relative velocity estimation
  - Sensor fusion

  ### Relative Navigation

  - Full relative state estimation
  - Vision-based relative navigation
  - Robust estimation under measurement uncertainty

  ### Spacecraft Dynamics

  - 6-DoF translational and rotational dynamics
  - Attitude dynamics
  - Orbital / relative orbital dynamics
  - Thruster constraints

  ### Advanced GNC

  - Controller tuning studies
  - Nonlinear control
  - Model predictive control
  - Guidance and trajectory planning
  - Thruster allocation

  ### Robustness and Research Evaluation

  - Sensor noise
  - Image degradation
  - Communication latency
  - Disturbances
  - Monte Carlo experiments
  - Larger statistical evaluation
  - Failure-mode analysis

  These extensions represent a future research direction rather than completed functionality.

  ---

  ## Engineering Philosophy

  This project follows a staged development approach:

  ```text
  Phase 1–6
  Build the system
        ↓
  Phase 7
  Prove the system works
        ↓
  Phase 8
  Make the project presentable and reproducible
        ↓
  Future
  Extend toward research-grade spacecraft robotics
  ```

  The current priority is **engineering competence and reproducibility**, rather than adding advanced research features before the MVP is well documented and validated.

  ---

  ## Project Status

  **MVP: 🟢 Complete**

  The project has demonstrated a working end-to-end closed-loop vision-based docking prototype with:

  - ROS 2 communication
  - Computer vision target detection
  - Relative position estimation
  - Proportional visual servoing
  - Simulated spacecraft motion
  - Docking detection
  - Safety handling
  - Experiment logging
  - Controlled evaluation
  - Result analysis
  - Documentation

  The next stage is to improve repository presentation, reproducibility, and documentation before considering research-grade extensions.

  ---

  ## License

  This project is intended as a project-based learning and engineering development project.