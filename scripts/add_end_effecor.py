# adding end effector to the urdf files

import argparse
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path


def attach_hand(base_robot_root, hand_urdf_path, effector_link_name):
    """
    Attaches a hand URDF to the base robot's XML tree.
    """
    if not hand_urdf_path or not hand_urdf_path.exists():
        print(f"Warning: Hand URDF not found at {hand_urdf_path}, skipping.")
        return

    hand_tree = ET.parse(hand_urdf_path)
    hand_root = hand_tree.getroot()

    # The first link in the hand's URDF is assumed to be its base link.
    hand_base_link = hand_root.find("link").get("name")

    hand_base_joint = hand_base_link.replace("_link", "_joint")

    # Copy all link and joint elements from the hand to the base robot.
    for element in hand_root.findall("link") + hand_root.findall("joint"):
        base_robot_root.append(element)

    # Create the new fixed joint to attach the hand.
    joint = ET.Element("joint", name=hand_base_joint, type="fixed")
    ET.SubElement(joint, "parent", link=effector_link_name)
    ET.SubElement(joint, "child", link=hand_base_link)
    ET.SubElement(joint, "origin", rpy="0 0 0", xyz="0 0 0")
    base_robot_root.append(joint)
    print(f"  Attached {hand_urdf_path.name} to {effector_link_name}")


def get_hand_file(hand_folder_path, hand_side):
    """
    Returns the path to the hand URDF file based on the side (left/right).
    """
    # check if left and right in file name for all file inside the folder
    hand_side = hand_side.lower()
    if hand_side not in ["left", "right"]:
        print(f"Error: hand_side must be 'left' or 'right', got '{hand_side}'")
        return None

    urdf_path = hand_folder_path / "urdf"

    for file in urdf_path.glob("*.urdf"):
        if hand_side in file.name:
            return file, file.name.replace(".urdf", "")


def copy_hand_stl(hand_folder_path, robot_urdf_path):
    """
    Copies the hand STL files to the same directory as the robot URDF.
    """
    stl_path = hand_folder_path / "meshes"
    robot_mesh_dir = robot_urdf_path.parent.parent / "meshes"

    if not stl_path.exists() or not stl_path.is_dir():
        print(
            f"Warning: Hand meshes directory not found at {stl_path}, skipping STL copy."
        )
        return

    shutil.copytree(stl_path, robot_mesh_dir, dirs_exist_ok=True)


def generate_urdf(base_robot_path, hand_folder_path):
    """
    Generates a single combined URDF by attaching hands to a base robot.
    """
    base_robot_path = Path(base_robot_path)
    if not base_robot_path.exists():
        print(f"Error: Base robot URDF not found at {base_robot_path}")
        return

    hand_folder_path = Path(hand_folder_path)
    if not hand_folder_path.is_dir():
        print(f"Error: Hand folder not found at {hand_folder_path}")
        return

    base_tree = ET.parse(base_robot_path)
    base_root = base_tree.getroot()

    # Define paths for left and right hand URDFs
    left_hand_path, left_hand_name = get_hand_file(hand_folder_path, "left")
    right_hand_path, right_hand_name = get_hand_file(hand_folder_path, "right")

    print(left_hand_name, right_hand_name)
    # Attach hands
    attach_hand(base_root, left_hand_path, "left_end_effector_link")
    attach_hand(base_root, right_hand_path, "right_end_effector_link")

    # Copy hand STL files to the robot's mesh directory
    copy_hand_stl(hand_folder_path, base_robot_path)

    left_hand_type = left_hand_name.replace("left_", "")
    right_hand_type = right_hand_name.replace("right_", "")

    if left_hand_type == right_hand_type:
        output_name = f"{base_robot_path.stem}_{left_hand_type}.urdf"
    else:
        output_name = f"{base_robot_path.stem}_{left_hand_type}_{right_hand_type}.urdf"

    # Write the combined URDF to a new file
    # output_name = f"{base_robot_path.stem}_with_hands.urdf"
    output_path = base_robot_path.parent.parent / "urdf" / output_name
    if not output_path.parent.exists():
        output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write the file
    base_tree.write(output_path, encoding="utf-8", xml_declaration=True)
    print(f"\nGenerated combined URDF at: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Combine a base robot URDF with left and right hand URDFs."
    )
    parser.add_argument("urdf_path", type=str, help="Path to the base robot URDF file.")
    parser.add_argument(
        "hand_folder",
        type=str,
        help="Path to the folder containing hand URDFs (expected to be named left.urdf and right.urdf).",
    )

    args = parser.parse_args()
    generate_urdf(args.urdf_path, args.hand_folder)
