import glob
import os
import shutil

import pymeshlab


# using meshlab to do the mesh compression
def compress_mesh(input_file, output_file, targetfacenum=20000):
    """
    Compress a mesh file using pymeshlab.

    :param input_file: Path to the input mesh file.
    :param output_file: Path to save the compressed mesh file.
    :param targetfacenum: Target facenum for the compressed mesh (default is 20000).
    """
    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(input_file)

    # Get current face count
    current_faces = ms.current_mesh().face_number()
    print(f"Processing {input_file}: {current_faces} faces")

    # Skip if already below target
    if current_faces <= targetfacenum:
        print(
            f"Skipping {input_file}: already has {current_faces} faces (target: {targetfacenum})"
        )
        return False

    # Apply simplification filter
    ms.apply_filter(
        "meshing_decimation_quadric_edge_collapse",
        targetfacenum=targetfacenum,
        preserveboundary=True,
        preservenormal=True,
    )

    # Save the compressed mesh
    ms.save_current_mesh(output_file)
    new_faces = ms.current_mesh().face_number()
    print(f"Compressed {input_file}: {current_faces} -> {new_faces} faces")
    return True


def compress_folder(folder_path, targetfacenum=20000, output_folder=None):
    """
    Compress all STL files in a folder and store them in a specified output folder.
    If a mesh is below the target face count, it will be copied without modification.

    :param folder_path: Path to the folder containing STL files.
    :param targetfacenum: Target number of faces for compression.
    :param output_folder: Path to the folder where compressed files will be saved.
    """
    # Find all STL files (case insensitive)
    stl_files = []
    for ext in ["*.stl", "*.STL"]:
        stl_files.extend(glob.glob(os.path.join(folder_path, ext)))

    if not stl_files:
        print(f"No STL files found in {folder_path}")
        return

    print(f"Found {len(stl_files)} STL files to process")

    if output_folder:
        os.makedirs(output_folder, exist_ok=True)

    processed = 0
    copied = 0
    errors = 0

    for stl_file in stl_files:
        base_name = os.path.basename(stl_file)
        output_file = os.path.join(output_folder or folder_path, base_name)

        try:
            result = compress_mesh(stl_file, output_file, targetfacenum)
            if result:
                processed += 1
            else:
                # copy unchanged mesh if compression skipped
                shutil.copy2(stl_file, output_file)
                print(f"Copied (uncompressed): {stl_file} -> {output_file}")
                copied += 1
        except Exception as e:
            print(f"Error processing {stl_file}: {e}")
            errors += 1
            continue

    print(
        f"\nSummary: {processed} files compressed, {copied} files copied, {errors} errors"
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Compress mesh files using pymeshlab.")

    # Add mutually exclusive group for single file vs folder processing
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--file",
        nargs=2,
        metavar=("INPUT", "OUTPUT"),
        help="Process single file: INPUT_FILE OUTPUT_FILE",
    )
    group.add_argument(
        "--folder",
        "-f",
        type=str,
        metavar="FOLDER_PATH",
        help="Process all STL files in folder",
    )

    parser.add_argument(
        "-tn",
        "--targetfacenum",
        type=int,
        default=20000,
        help="Target number of faces for the compressed mesh (default is 20000).",
    )
    parser.add_argument(
        "-o",
        "--output_folder",
        type=str,
        default=None,
        help="Optional folder to store compressed files (default: same as input folder)",
    )

    args = parser.parse_args()

    if args.file:
        input_file, output_file = args.file
        compress_mesh(input_file, output_file, args.targetfacenum)
    elif args.folder:
        compress_folder(args.folder, args.targetfacenum, args.output_folder)
