import os
import shutil

def move_csv_files(repo_path, entry):
    """
    Scans the given repository for CSV files and moves them to a new directory
    within the same parent directory.
    
    :param repo_path: Path to the repository
    """
    if not os.path.exists(repo_path):
        print("Repository path does not exist.")
        return
    
    # Define new directory name
    parent_dir = os.path.dirname(repo_path)
    csv_dir = os.path.join(parent_dir, f"csv_files_{entry}")
    
    # Create directory if it doesn't exist
    os.makedirs(csv_dir, exist_ok=True)
    
    # Walk through the repository and find CSV files
    for root, _, files in os.walk(repo_path):
        for file in files:
            print("FILE", file)
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)
                new_path = os.path.join(csv_dir, file)
                
                # Move the file
                shutil.copy2(file_path, new_path)
                print(f"Moved: {file_path} -> {new_path}")

# Example usage
parent = "/eagle/projects/FoundEpidem/astroka/rpe_2/20x_original/ind_channels_seg/ch3"
for entry in os.listdir(parent):
    full_path = os.path.join(parent, entry)
    move_csv_files(full_path, entry)
# move_csv_files("/eagle/projects/FoundEpidem/astroka/rpe/week_nine/ind_channels_seg_control/ch4/Compound_12")
