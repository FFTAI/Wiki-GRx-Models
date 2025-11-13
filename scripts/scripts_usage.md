# Scripts Usage Guide

The `scripts/` folder provides a comprehensive set of Python tools for URDF manipulation, analysis, and enhancement. These scripts form a complete pipeline for extracting parameters, adding motor dynamics, and optimizing robot models.

## Available Scripts

### Core Analysis Scripts
- **`urdf_loader.py`**: Visualizes URDF files using Pinocchio and MeshCat for 3D preview and collision detection
- **`urdf_parameter.py`**: Extracts parameters from URDF files (mass, effort, joint limits, velocity). Outputs `{urdf_name}_parameters.json`

### Manipulation Scripts
- **`add_end_effecor.py`**: Combines a base robot URDF with hand URDFs (left/right) to create complete humanoid models

### Utility Scripts
- **`mesh_compresser.py`**: Compresses mesh files using PyMeshLab to reduce polygon count and file sizes

---

## Detailed Usage

### 1. urdf_loader.py

**Purpose**: Load and visualize URDF files using Pinocchio and MeshCat with 3D rendering and collision mesh display.

**Dependencies**: 
- `pinocchio`
- `meshcat`

**Usage**:
```bash
python urdf_loader.py <urdf_path> [options]
```

**Arguments**:
- `urdf_path` (required): Path to the URDF file to visualize
- `--no-visualize`: Load robot without visualization
- `--package-dirs`: Additional package directories for mesh loading (space-separated)
- `--duration`: Duration to keep visualization open in seconds (default: 5.0)

**Examples**:
```bash
# Basic visualization (5 seconds)
python urdf_loader.py GRX/GR1/GR1T1/urdf/GR1T1_nohand.urdf

# Extended visualization (30 seconds)
python urdf_loader.py GRX/GR1/GR1T1/urdf/GR1T1_nohand.urdf --duration 30.0

# Load without visualization
python urdf_loader.py GRX/GR2/gr2v3_8_7/basic_urdf/gr2v3_8_7.urdf --no-visualize

# With custom package directories
python urdf_loader.py my_robot.urdf --package-dirs /path/to/meshes /another/path
```

**Features**:
- Loads URDF with free-flyer root joint
- Displays visual and collision meshes
- Interactive 3D visualization in browser via MeshCat
- Supports custom mesh package directories

---

### 2. urdf_parameter.py

**Purpose**: Extract and export robot parameters from URDF files to structured JSON format.

**Usage**:
```bash
python urdf_parameter.py <urdf_path> [options]
```

**Arguments**:
- `urdf_path` (required): Path to the URDF file
- `--mass`: Extract mass values from links
- `--effort`: Extract effort (torque) limits from joints
- `--limit`: Extract joint position limits (upper and lower)
- `--velocity`: Extract joint velocity limits

**Examples**:
```bash
# Extract all parameters
python urdf_parameter.py GRX/GR1/GR1T1/urdf/GR1T1_nohand.urdf --mass --effort --limit --velocity

# Extract only mass and effort
python urdf_parameter.py GRX/GR2/gr2v3_8_7/basic_urdf/gr2v3_8_7.urdf --mass --effort

# Extract joint limits only
python urdf_parameter.py my_robot.urdf --limit --velocity
```

**Output**:
Creates a JSON file named `{urdf_name}_parameters.json` in the same directory as the URDF file with structure:
```json
{
    "robot_name": "robot_name",
    "total_mass": 45.2,
    "links": {
        "link_name": {
            "actuator": "",
            "mass": "2.5"
        }
    },
    "joints": {
        "joint_name": {
            "child_link": "child_link_name",
            "effort": "100.0",
            "upper_limit": "1.57",
            "lower_limit": "-1.57",
            "velocity": "3.14"
        }
    }
}
```

---

### 3. add_end_effecor.py

**Purpose**: Combine a base robot URDF with left and right hand URDFs to create a complete humanoid robot model.

**Usage**:
```bash
python add_end_effecor.py <urdf_path> <hand_folder>
```

**Arguments**:
- `urdf_path` (required): Path to the base robot URDF file (e.g., robot without hands)
- `hand_folder` (required): Path to the folder containing hand URDF and mesh files

**Expected Hand Folder Structure**:
```
hand_folder/
├── urdf/
│   ├── left_hand_name.urdf    # Must contain "left" in filename
│   └── right_hand_name.urdf   # Must contain "right" in filename
└── meshes/
    └── [hand mesh files]
```

**Examples**:
```bash
# Add Fourier hands to GR1T1
python add_end_effecor.py \
    GRX/GR1/GR1T1/urdf/GR1T1_nohand.urdf \
    Dexterous_hand/fourier_hand_6dof

# Add inspire hands to GR1T2
python add_end_effecor.py \
    GRX/GR1/GR1T2/urdf/GR1T2_nohand.urdf \
    path/to/inspire_hand_folder
```

**Output**:
- Creates a new URDF file in the base robot's urdf directory
- Naming convention:
  - Same hand type: `{robot_name}_{hand_type}.urdf`
  - Different hand types: `{robot_name}_{left_hand}_{right_hand}.urdf`
- Copies hand mesh files to robot's mesh directory

**How It Works**:
1. Parses base robot URDF
2. Identifies left and right hand URDF files (by filename)
3. Attaches hands to `left_end_effector_link` and `right_end_effector_link` with fixed joints
4. Copies hand meshes to robot mesh directory
5. Writes combined URDF file

**Requirements**:
- Base robot must have `left_end_effector_link` and `right_end_effector_link`
- Hand URDF filenames must contain "left" or "right"
- First link in hand URDF is assumed to be the hand base link

---

### 4. mesh_compresser.py

**Purpose**: Compress STL mesh files using quadric edge collapse decimation to reduce polygon count and file size.

**Dependencies**:
- `pymeshlab`

**Usage**:

**Single File Mode**:
```bash
python mesh_compresser.py --file <input_file> <output_file> [options]
```

**Folder Mode**:
```bash
python mesh_compresser.py --folder <folder_path> [options]
```

**Arguments**:
- `--file INPUT OUTPUT`: Process a single mesh file
- `--folder FOLDER_PATH` or `-f FOLDER_PATH`: Process all STL files in folder
- `-tn` or `--targetfacenum`: Target number of faces (default: 20000)
- `-o` or `--output_folder`: Output folder for compressed files (default: same as input)

**Examples**:
```bash
# Compress single file
python mesh_compresser.py --file input.stl output.stl --targetfacenum 10000

# Compress all meshes in folder (default 20k faces)
python mesh_compresser.py --folder GRX/GR1/GR1T1/meshes/fourier_hand_6dof

# Compress to different output folder with custom target
python mesh_compresser.py -f meshes/original -o meshes/compressed -tn 15000

# Aggressive compression (5k faces)
python mesh_compresser.py --folder my_meshes --targetfacenum 5000
```

**Features**:
- Quadric edge collapse decimation algorithm
- Preserves mesh boundaries and normals
- Automatically skips meshes already below target face count
- Batch processing of entire directories
- Summary statistics (compressed, copied, errors)

**Behavior**:
- If mesh has fewer faces than target: copied without modification
- If mesh has more faces than target: compressed to target face count
- Supports both `.stl` and `.STL` file extensions

**Typical Use Cases**:
- Reducing mesh complexity for faster simulation
- Optimizing models for real-time visualization
- Reducing file sizes for version control
- Preparing models for embedded systems

---

## Common Workflows

### Workflow 1: Create Complete Robot with Hands
```bash
# 1. Start with base robot (no hands)
# 2. Add hands to create complete model
python add_end_effecor.py \
    GRX/GR1/GR1T1/urdf/GR1T1_nohand.urdf \
    Dexterous_hand/fourier_hand_6dof

# 3. Visualize the result
python urdf_loader.py GRX/GR1/GR1T1/urdf/GR1T1_fourier_hand_6dof.urdf --duration 30

# 4. Extract parameters for analysis
python urdf_parameter.py GRX/GR1/GR1T1/urdf/GR1T1_fourier_hand_6dof.urdf --mass --effort --limit
```

### Workflow 2: Optimize Existing Robot Model
```bash
# 1. Extract current parameters
python urdf_parameter.py my_robot.urdf --mass --effort --limit --velocity

# 2. Compress meshes for better performance
python mesh_compresser.py --folder my_robot/meshes --targetfacenum 10000 -o my_robot/meshes_optimized

# 3. Update URDF mesh paths (manual step) and visualize
python urdf_loader.py my_robot_optimized.urdf
```

### Workflow 3: Model Analysis and Validation
```bash
# 1. Load and inspect visually
python urdf_loader.py robot.urdf --duration 60

# 2. Extract all parameters
python urdf_parameter.py robot.urdf --mass --effort --limit --velocity

# 3. Review JSON output for validation
cat robot_parameters.json
```

---

## Installation Requirements

Install required Python packages:

```bash
# For urdf_loader.py
pip install pin pinocchio meshcat

# For urdf_parameter.py (standard library only)
# No additional packages required

# For add_end_effecor.py (standard library only)
# No additional packages required

# For mesh_compresser.py
pip install pymeshlab
```

---

## Tips and Best Practices

1. **Visualization**: Use longer `--duration` values when you need time to inspect the robot from different angles
2. **Parameter Extraction**: Extract only needed parameters to keep JSON files focused and readable
3. **Mesh Compression**: 
   - Start with higher face counts (15k-20k) for high-quality visualization
   - Use lower face counts (5k-10k) for real-time simulation
   - Always backup original meshes before compression
4. **Hand Attachment**: 
   - Ensure base robot has correct end effector link names
   - Verify hand URDF files follow naming conventions
5. **File Organization**: Keep generated files (JSONs, combined URDFs) organized in appropriate directories

---

## Troubleshooting

**Issue**: `urdf_loader.py` shows "URDF file not found"
- **Solution**: Use absolute paths or ensure working directory is correct

**Issue**: `mesh_compresser.py` produces low-quality meshes
- **Solution**: Increase `--targetfacenum` value

**Issue**: `add_end_effecor.py` cannot find hand files
- **Solution**: Ensure hand URDF filenames contain "left" or "right"

**Issue**: Visualization window doesn't open
- **Solution**: Check that MeshCat can bind to network port; try restarting the script

**Issue**: Missing meshes in visualization
- **Solution**: Verify `--package-dirs` points to correct mesh directories