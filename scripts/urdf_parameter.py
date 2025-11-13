import argparse
import json
import os
import xml.etree.ElementTree as ET


def extract_urdf_parameters(
    urdf_path,
    extract_mass=False,
    extract_effort=False,
    extract_limit=False,
    extract_velocity=False,
):
    """
    Extracts specified parameters from a URDF file and saves them to a structured JSON file
    in the same directory as the URDF file.

    :param urdf_path: Path to the URDF file.
    :param extract_mass: Flag to extract mass.
    :param extract_effort: Flag to extract effort.
    :param extract_limit: Flag to extract joint limits (upper and lower).
    :param extract_velocity: Flag to extract joint velocity limits.
    """
    # Parse the URDF file
    tree = ET.parse(urdf_path)
    root = tree.getroot()
    robot_name = root.get("name")

    # Extract directory from the URDF path
    urdf_dir = os.path.dirname(urdf_path)
    urdf_filename = os.path.splitext(os.path.basename(urdf_path))[0]
    output_file = os.path.join(urdf_dir, f"{urdf_filename}_parameters.json")

    # Dictionary to store extracted data
    urdf_data = {"robot_name": robot_name}
    urdf_data = {"total_mass": 0.0}

    if extract_mass:
        total_mass = 0.0

    # Extract link data
    urdf_data["links"] = {}
    for link in root.iter("link"):
        link_name = link.get("name")

        # Initialize each link with an empty actuator field
        urdf_data["links"][link_name] = {"actuator": ""}

        if extract_mass:
            mass_element = link.find("inertial/mass")
            if mass_element is not None:
                mass = mass_element.get("value")
                urdf_data["links"][link_name]["mass"] = mass
                try:
                    total_mass += float(mass)
                except ValueError:
                    print(
                        f"Warning: could not convert mass '{mass}' of link '{link_name}' to float."
                    )

    if extract_mass:
        urdf_data["total_mass"] = total_mass

    # Extract joint data
    urdf_data["joints"] = {}
    for joint in root.iter("joint"):
        joint_name = joint.get("name")
        if joint_name not in urdf_data["joints"]:
            urdf_data["joints"][joint_name] = {}

        # Extract child link
        child = joint.find("child")
        if child is not None:
            child_link = child.get("link")
            urdf_data["joints"][joint_name]["child_link"] = child_link

        # Extract limit parameters
        limit = joint.find("limit")
        if limit is not None:
            if extract_effort:
                effort = limit.get("effort")
                if effort is not None:
                    urdf_data["joints"][joint_name]["effort"] = effort

            if extract_limit:
                upper_limit = limit.get("upper")
                lower_limit = limit.get("lower")
                if upper_limit is not None and lower_limit is not None:
                    urdf_data["joints"][joint_name]["upper_limit"] = upper_limit
                    urdf_data["joints"][joint_name]["lower_limit"] = lower_limit

            if extract_velocity:
                velocity = limit.get("velocity")
                if velocity is not None:
                    urdf_data["joints"][joint_name]["velocity"] = velocity

    # Save data to JSON file
    with open(output_file, "w") as jsonfile:
        json.dump(urdf_data, jsonfile, indent=4)

    print(f"URDF parameters extracted successfully to: {output_file}")


if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Extract parameters from a URDF file.")
    parser.add_argument("urdf_path", type=str, help="Path to the URDF file.")
    parser.add_argument("--mass", action="store_true", help="Extract mass values.")
    parser.add_argument("--effort", action="store_true", help="Extract effort values.")
    parser.add_argument(
        "--limit", action="store_true", help="Extract joint limits (upper and lower)."
    )
    parser.add_argument(
        "--velocity", action="store_true", help="Extract joint velocity limits."
    )
    args = parser.parse_args()

    # Call the function
    extract_urdf_parameters(
        urdf_path=args.urdf_path,
        extract_mass=args.mass,
        extract_effort=args.effort,
        extract_limit=args.limit,
        extract_velocity=args.velocity,
    )
