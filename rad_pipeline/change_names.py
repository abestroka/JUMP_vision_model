import pandas as pd
import os
import random
import string
import shutil
import argparse
import numpy as np

def change_names(target, dst_dir, src_dir):
    
    src_images = os.listdir(src_dir)

    for image in src_images:
        curr_path = os.path.join(src_dir, image)
    #         if image in dst_images:
        # rename so no overwrite
        new_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))
        new_name = new_name + ".png"
        new_path = os.path.join(src_dir, new_name)
        os.rename(curr_path, new_path)

        shutil.copy(new_path, dst_dir)



def main(args):
    target = vars(args)["target"]
    src_dir = '/home/astroka/workspace/JUMP_vision_model/rad_pipeline/segmented_image_temp/'+target
    # dst_path = "/eagle/projects/FoundEpidem/astroka/top_10/segmented_images/"+target + "/"
    dst_path = "/eagle/projects/FoundEpidem/astroka/pilot_imgs/segmented_images/"+target + "/"

    if os.path.isdir(dst_path) == False:
        os.mkdir(dst_path)
    change_names(target, dst_path, src_dir)
    shutil.rmtree(src_dir)






if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
    "-t",
    "--target",
    help="target folder name",
    type=str,
    required=True,
    )


    args = parser.parse_args()

    main(args)