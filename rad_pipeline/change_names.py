import pandas as pd
import os
import random
import string
import shutil
import argparse
import numpy as np

def change_names(target, dst_dir, src_dir, name):
    
    src_images = os.listdir(src_dir)

    for image in src_images:
        if '.png' in image:
            curr_path = os.path.join(src_dir, image)
            # print('CURRPATH', curr_path)
        #         if image in dst_images:
            # rename so no overwrite
            # new_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))
            # new_name = new_name + ".png"
            # new_path = os.path.join(src_dir, new_name)
            # os.rename(curr_path, new_path)
            new_name = name + ".png"
            new_path = os.path.join(src_dir, new_name)
            # print("NEWPATH", new_path)
            os.rename(curr_path, new_path)
            # print("NEWPATH", new_path)
            shutil.copy(new_path, dst_dir)

        elif 'Image' in image:
            curr_path = os.path.join(src_dir, image)
        #         if image in dst_images:
            # rename so no overwrite
            # new_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))
            # new_name = new_name + ".csv"
            # new_path = os.path.join(src_dir, new_name)
            # os.rename(curr_path, new_path)
            df = pd.read_csv(curr_path)
            totalarea = df['AreaOccupied_TotalArea_Cells'][0]
            cellarea = df['AreaOccupied_AreaOccupied_Cells'][0]
            confluency = float(cellarea/totalarea)


            with open(dst_dir+name+"_"+"confluency.txt", 'w') as file:
                file.write(str(confluency))
            file.close()

            new_name = name + ".csv"
            new_path = os.path.join(src_dir, new_name)
            os.rename(curr_path, new_path)
            shutil.copy(new_path, dst_dir)




def main(args):
    target = vars(args)["target"]
    name = vars(args)["name"]
    seg_image_temp = vars(args)["src"]
    dst_image_path = vars(args)["dst"]
    # src_dir = '/home/astroka/workspace/JUMP_vision_model/rad_pipeline/segmented_image_temp/'+target
    src_dir = '/home/astroka/workspace/JUMP_vision_model/rad_pipeline/'+seg_image_temp+'/'+target
    # src_dir = '/eagle/FoundEpidem/astroka/ten_week/week_one/results/huvec_rad/'+target
    # dst_path = "/eagle/projects/FoundEpidem/astroka/top_10/segmented_images/"+target + "/"

    # dst_path = "/eagle/projects/FoundEpidem/astroka/pilot_imgs/segmented_images/"+target + "/"
    # dst_path = '/eagle/FoundEpidem/astroka/ten_week/week_one/results/huvec_rad/'+target +"/"
    # dst_path = '/eagle/FoundEpidem/astroka/ten_week/week_one/results/fib_rad/'+target +"/"
    # dst_path = '/eagle/FoundEpidem/astroka/ten_week/week_one/results/huvec_control/'+target +"/"
    dst_path = '/eagle/FoundEpidem/astroka/ten_week/week_one/results/'+dst_image_path+'/'+target +"/"
    # dst_path = '/eagle/FoundEpidem/astroka/ten_week/week_one/test/'+dst_image_path+'/'+target +"/"





    if os.path.isdir(dst_path) == False:
        os.mkdir(dst_path)
    change_names(target, dst_path, src_dir, name)
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
    parser.add_argument(
    "-n",
    "--name",
    help="target folder name",
    type=str,
    required=True,
    )

    parser.add_argument(
    "-s",
    "--src",
    help="target folder name",
    type=str,
    required=True,
    )
    parser.add_argument(
    "-d",
    "--dst",
    help="target folder name",
    type=str,
    required=True,
    )


    args = parser.parse_args()

    main(args)