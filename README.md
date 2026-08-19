# Vision-Based Autonomous Spacecraft Docking

A project-based learning project for developing a vision-based autonomous spacecraft docking system using ROS 2, computer vision, simulation, estimation, and control.

## Goal

Develop an autonomous spacecraft docking system that can:

1. Detect a target spacecraft using a camera
2. Estimate the relative pose between the chaser and target
3. Estimate relative motion
4. Control the chaser spacecraft toward the docking port
5. Perform autonomous docking in simulation

## Learning Areas

- ROS 2
- C++ / Python
- Computer Vision
- Camera Models
- Pose Estimation
- Coordinate Frames
- State Estimation
- Relative Navigation
- Visual Servoing
- Guidance, Navigation and Control
- Spacecraft Dynamics
- Autonomous Docking

## Project Status

🚧 Initial setup

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

## Repository Structure

```text
docs/          Documentation and notes
ros2_ws/       ROS 2 packages
simulation/    Simulation environments
experiments/   Experiment configurations and results
tests/         Automated tests
