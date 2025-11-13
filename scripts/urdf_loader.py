import argparse
import os
import time

import pinocchio as pin
from pinocchio.visualize import MeshcatVisualizer


def robot_loader(urdf_path, visualize=True, package_dirs=None):
    if not os.path.isfile(urdf_path):
        current_dir = os.getcwd()
        print(
            f"wrong path, current path: {current_dir}, the path defined is {urdf_path}"
        )
        assert os.path.isfile(urdf_path), "URDF file not found."

    # Set default package directories if none provided
    if package_dirs is None:
        package_dirs = [
            "/home/fourier/gitlab/supermodels/Dexterous_Hand/Fourier_hand_6dof/urdf/"
        ]

    # Load the robot model
    robot = pin.RobotWrapper.BuildFromURDF(
        filename=urdf_path,
        package_dirs=package_dirs,
        root_joint=pin.JointModelFreeFlyer(),
    )

    # Rebuild data for the robot
    robot.rebuildData()
    robot.q0 = pin.neutral(robot.model)
    configuration = robot.q0

    # Initialize the visualizer
    viz = None
    if visualize:
        viz = MeshcatVisualizer(robot.model, robot.collision_model, robot.visual_model)
        viz.initViewer(open=True)
        viz.loadViewerModel()
        viz.display(configuration)

        # Display collision meshes
        viz.displayCollisions(True)

    return viz


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Load and visualize URDF files using Pinocchio and MeshCat"
    )
    parser.add_argument(
        "urdf_path", type=str, help="Path to the URDF file to visualize"
    )
    parser.add_argument(
        "--no-visualize", action="store_true", help="Load robot without visualization"
    )
    parser.add_argument(
        "--package-dirs",
        nargs="+",
        type=str,
        help="Additional package directories for mesh loading",
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=5.0,
        help="Duration to keep visualization open (seconds), default: 5.0",
    )

    args = parser.parse_args()

    print(f"Loading URDF: {args.urdf_path}")

    # Load and visualize the robot
    visualizer = robot_loader(
        urdf_path=args.urdf_path,
        visualize=not args.no_visualize,
        package_dirs=args.package_dirs,
    )

    if visualizer:
        print(f"Visualization started. Keeping open for {args.duration} seconds...")
        time.sleep(args.duration)
        print("Visualization complete.")
    else:
        print("Robot loaded successfully (no visualization).")
