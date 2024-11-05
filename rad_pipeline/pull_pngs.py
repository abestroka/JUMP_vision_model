import os
import shutil

def copy_png_images(src_dir, dest_dir):
    # Walk through the source directory and its subdirectories
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.lower().endswith('.png'):  # Check if the file is a PNG image
                # Construct full source file path
                src_file = os.path.join(root, file)
                
                # Construct corresponding destination directory and file path
                # Create directories in the destination if they don't exist
                rel_dir = os.path.relpath(root, src_dir)
                dest_subdir = os.path.join(dest_dir, rel_dir)
                os.makedirs(dest_subdir, exist_ok=True)
                
                # Construct destination file path
                dest_file = os.path.join(dest_subdir, file)
                
                # Copy the PNG file to the destination
                shutil.copy(src_file, dest_file)
                print(f"Copied {src_file} to {dest_file}")

# Example usage
src_directory = '/eagle/FoundEpidem/astroka/fib_and_htert/week_three/results/fib_control'  # Replace with your source directory path
dest_directory = '/eagle/FoundEpidem/astroka/fib_and_htert/week_three/results_png_only/fib_control'  # Replace with your destination directory path

copy_png_images(src_directory, dest_directory)
