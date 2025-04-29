[简体中文](README.md) | English

# Wiki-GRx-Models

<img src="./pictures/n1.png" width="300" height="300" />

Welcome to the GRx Robot Model Repository!
This repository provides the Unified Robot Description Format (URDF) files for the GRx robot,
enabling enthusiasts and developers to explore, modify, and extend the capabilities of this robotic platform.

## Model List

**N1**:

- N1_raw: The `urdf` without rotor inertia.
- N1_rotor: The `urdf` with rotor inertia.

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
# Display the GRMini model with fourier hand
cd ./GRX/GRMini/GRMini/URDF/urdf
urdf-viz GRMini.urdf
```

---

Thank you for your interest in the Fourier Intelligence GRx Robot Repositories.
We hope you find this resource helpful in your robotics projects!
