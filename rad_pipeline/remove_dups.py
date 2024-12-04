import numpy as np
import os

path = '/eagle/FoundEpidem/astroka/yolo/rpe_rad_2'

for root, dirs, files in os.walk(path):
    print(f"Current Directory: {root}")
    
    # # List of directories in the current directory
    # for dir_name in dirs:
    #     print(f"  Directory: {os.path.join(root, dir_name)}")

    for file_name in files:
        # print(f"  File: {os.path.join(root, file_name)}")
        if ".png" in file_name:

            print(file_name[:9])