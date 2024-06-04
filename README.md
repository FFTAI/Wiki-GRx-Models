# Wiki-GRx-Models

<img src="./pictures/gr1t1_model.png" width="300" height="360" />
<img src="./pictures/gr1t2_model.png" width="300" height="360" />

[//]: # (![]&#40;./pictures/GR1T1.png&#41;)

Welcome to the GRx Robot Model Repository!
This repository provides the Unified Robot Description Format (URDF) files for the GRx robot,
enabling enthusiasts and developers to explore, modify, and extend the capabilities of this robotic platform.

## Overview

The Fourier Intelligence GRx series robot is a versatile and robust platform designed for a wide range of applications,
including research, education, and industrial automation. This repository contains the necessary URDF files
and associated resources to simulate and develop with the GRx robot using popular robotics software tools.

## Features

- **URDF Files**: Complete set of URDF files describing the GRx robots' kinematic and dynamic properties.
- **Visual Models**: High-quality 3D models for visualization in simulation environments.
- **Collision Models**: Optimized collision models for efficient simulation.
- **Issac Gym**: Support for NVIDIA Isaac Gym for reinforcement learning and robotics research.
- **Isaac Sim**: Support for NVIDIA Isaac Sim for high-fidelity simulation.

## Model Verification

To verify the model, you can use the `urdf-viz` tool to visualize the robot in 3D.

- https://github.com/openrr/urdf-viz

### Install with Cargo

```bash
sudo apt-get install cmake xorg-dev libglu1-mesa-dev
sudo apt install cargo
cargo install urdf-viz
```

### Display the Model

```bash
# Display the GR1T1 model
cd ./GR1/GR1T1/urdf
urdf-viz GR1T1.urdf

# Display the GR1T2 model
cd ./GR1/GR1T2/urdf
urdf-viz GR1T2.urdf
```

## MJCF Conversion

If you are interested in converting the URDF files to MuJoCo MJCF format, you can refer to the following repository:

- [Wiki-MJCF in Github](https://github.com/FFTAI/wiki-mjcf/)
- [Wiki-MJCF in Gitee](https://gitee.com/FourierIntelligence/wiki-mjcf/)

---

Thank you for your interest in the Fourier Intelligence GRx Robot Repositories.
We hope you find this resource helpful in your robotics projects!
