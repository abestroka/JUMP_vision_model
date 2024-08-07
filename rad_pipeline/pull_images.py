import pandas as pd
import os
import random
import string
import shutil
import argparse
import numpy as np

# import path


def pull_image(i, image_path, temp_image_path, target_name_path, image_name_path):

    sheet_path =  image_path[:-6]+"all_images.xlsx"
    # sheet_path = image_path
    sheet = pd.read_excel(sheet_path)
    print(sheet)


    dna = sheet.loc[i, 'dna']
    print("i", i)
    print("DNA", dna)
    # print(dna[:12])
    shutil.copy(image_path+"/"+str(dna), temp_image_path)
    os.rename(temp_image_path+"/"+str(dna), temp_image_path+"/"+"dna.tiff")

    rna = sheet.loc[i, 'rna']
    shutil.copy(image_path+"/"+str(rna), temp_image_path)
    os.rename(temp_image_path+"/"+str(rna), temp_image_path+"/"+"rna.tiff")

    er = sheet.loc[i, 'er']
    shutil.copy(image_path+"/"+str(er), temp_image_path)
    os.rename(temp_image_path+"/"+str(er), temp_image_path+"/"+"er.tiff")

    agp = sheet.loc[i, 'agp']
    shutil.copy(image_path+"/"+str(agp), temp_image_path)
    os.rename(temp_image_path+"/"+str(agp), temp_image_path+"/"+"agp.tiff")

    mito = sheet.loc[i, 'mito']
    shutil.copy(image_path+"/"+str(mito), temp_image_path)
    os.rename(temp_image_path+"/"+str(mito), temp_image_path+"/"+"mito.tiff")

    treatment = sheet.loc[i, 'treatment']
    with open(target_name_path, 'w') as file:
        file.write(str(treatment))
    file.close()

    name = dna[:12]
    print("PULL NAME", name)
    with open(image_name_path, 'w') as file:
        file.write(str(name))
    file.close()








def main(args):
    # meta = pd.read_csv("/eagle/projects/FoundEpidem/astroka/top_ten_100_each_metadata.csv")
    # meta = pd.read_csv("/eagle/projects/FoundEpidem/astroka/linked_metadata.csv")
    index = vars(args)["index"]
    image_path = vars(args)["path"]
    temp = vars(args)["temp"]
    seg = vars(args)["seg"]
    temp_image_path =  "/home/astroka/workspace/JUMP_vision_model/rad_pipeline/"+temp
    target_name_path =  "/home/astroka/workspace/JUMP_vision_model/rad_pipeline/target_name.txt"
    image_name_path =  "/home/astroka/workspace/JUMP_vision_model/rad_pipeline/image_name.txt"
    # segmented_image_path = "/eagle/projects/FoundEpidem/astroka/top_10/segmented_images"
    # segmented_image_path = "/eagle/projects/FoundEpidem/astroka/pilot_imgs/segmented_images"
    segmented_image_path = "/home/astroka/workspace/JUMP_vision_model/rad_pipeline/"+seg

    if os.path.isdir(temp_image_path) == False:
        os.mkdir(temp_image_path)
    
    pull_image(index, image_path, temp_image_path, target_name_path, image_name_path)
    if os.path.isdir(segmented_image_path) == False:
        os.mkdir(segmented_image_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
    "-i",
    "--index",
    help="number of samples to be taken from metadata",
    type=int,
    required=True,
    )
    parser.add_argument(
    "-p",
    "--path",
    help="number of samples to be taken from metadata",
    type=str,
    required=True,
    )
    parser.add_argument(
    "-t",
    "--temp",
    help="number of samples to be taken from metadata",
    type=str,
    required=True,
    )
    parser.add_argument(
    "-s",
    "--seg",
    help="number of samples to be taken from metadata",
    type=str,
    required=True,
    )


    args = parser.parse_args()

    main(args)