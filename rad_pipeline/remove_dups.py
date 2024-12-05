import numpy as np
import os
import argparse


# path = '/eagle/FoundEpidem/astroka/yolo/rpe_rad_2'


def remove_dups(path):
    print("PATH", path)
    for root, dirs, files in os.walk(path):
        print(f"Current Directory: {root}")
        
        # # List of directories in the current directory
        # for dir_name in dirs:
        #     print(f"  Directory: {os.path.join(root, dir_name)}")

        for file_name in files:
            # print(f"  File: {os.path.join(root, file_name)}")
            if ".png" in file_name and "p03" in file_name:
                name =  file_name[:9]
            else:
                to_del = os.path.join(root, file_name)
                print(to_del)
                os.remove(to_del)
                # print(file_name[:9])


def main(args):
    img_path = vars(args)["path"]
    print("MAIN")
    remove_dups(img_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
    "-p",
    "--path",
    help="path to images dir",
    type=str,
    required=True,
    )