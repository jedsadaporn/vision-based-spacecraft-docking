# Vision-Based Autonomous Spacecraft Docking

A project-based learning project for developing a vision-based autonomous spacecraft docking system using ROS 2, computer vision, simulation, estimation, and control.

## Goal

Build an end-to-end ROS 2 vision-based autonomous spacecraft docking system focused on practical Space Robotics and Robot Software Engineering skills. The first objective is to build a configurable, testable, and reproducible engineering MVP. Research-grade pose estimation, state estimation, spacecraft dynamics, advanced GNC, and robustness studies will be developed as later extensions.

Develop an autonomous spacecraft docking system that can:

1. Detect a target spacecraft using a camera
2. Estimate the relative pose between the chaser and target
3. Estimate relative motion
4. Control the chaser spacecraft toward the docking port
5. Perform autonomous docking in simulation

## Engineering Skills — MVP

- ROS 2
- Python
- Computer Vision
- Coordinate Frames
- Relative Position / Navigation
- Visual Servoing
- Basic GNC
- Robot Software Architecture
- Simulation / Gazebo
- Testing and Debugging
- Logging and Configuration
- Autonomous Docking

## Research Extensions

- 6-DoF Pose Estimation
- State Estimation / EKF
- Advanced Relative Navigation
- Spacecraft Dynamics
- Advanced GNC
- Robustness / Uncertainty
- Research-grade Experimental Evaluation

## Project Status

🟢 Core closed-loop MVP development

Core ROS 2 system          ✅
Docking logic              ✅
Safety / failure handling  ✅
Sanity validation          ✅
Engineering framework      🚧
Gazebo integration         ⏳
MVP final demo             ⏳
Research extensions        ⏳

## Planned Pipeline

Camera
  ↓
Target Detection
  ↓
Feature / Marker Detection
  ↓
Relative Pose Estimation
  ↓
State Estimation
  ↓
Guidance / Controller
  ↓
Spacecraft Motion
  ↓
Docking

### MVP Pipeline

Camera
↓
Target Detection
↓
Relative Position
↓
Visual Servoing / Controller
↓
Spacecraft Motion
↓
Docking

### Future Research Pipeline

Camera
↓
Feature / Marker Detection
↓
6-DoF Pose Estimation
↓
State Estimation
↓
Relative Navigation
↓
Advanced GNC
↓
Spacecraft Dynamics
↓
Robust Autonomous Docking

## Repository Structure

```text
docs/          Documentation and notes
ros2_ws/       ROS 2 packages
simulation/    Simulation environments
experiments/   Experiment configurations and results
tests/         Automated tests
