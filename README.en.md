[简体中文](README.md) | English

# Wiki-GRx-URDF

<img src="./pictures/n1.png" width="300" height="300" />

Welcome to the Fourier GRx Robot Model Repository!

This repository provides the Unified Robot Description Format (URDF) files for the Fourier GRx robot,
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
cd /path/to/your/project

cd N1/urdf
urdf-viz N1_raw.urdf
```

---

Thank you for your interest in Fourier's N1 robot project!
We hope this resource will provide strong support for your robotics development!
