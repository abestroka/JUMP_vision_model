import pandas as pd
import os
import random
import string
import shutil
import argparse
import numpy as np

# import path


def pull_image(i, image_path, temp_image_path, target_name_path):

    sheet_path =  image_path[:-6]+"all_images.xlsx"
    # sheet_path = image_path
    print(sheet_path)
    sheet = pd.read_excel(sheet_path)


    dna = sheet.loc[i, 'dna']
    print("DNA")
    print(dna)
    shutil.copy(image_path+"/"+str(dna), temp_image_path)
    os.rename(temp_image_path+"/"+str(dna), temp_image_path+"/"+"dna.tiff")

    rna = sheet.loc[i, 'rna']
    print("RNA")
    print(rna)
    shutil.copy(image_path+"/"+str(rna), temp_image_path)
    os.rename(temp_image_path+"/"+str(rna), temp_image_path+"/"+"rna.tiff")

    er = sheet.loc[i, 'er']
    print("ER")
    print(er)
    shutil.copy(image_path+"/"+str(er), temp_image_path)
    os.rename(temp_image_path+"/"+str(er), temp_image_path+"/"+"er.tiff")

    agp = sheet.loc[i, 'agp']
    print("AGP")
    print(agp)
    shutil.copy(image_path+"/"+str(agp), temp_image_path)
    os.rename(temp_image_path+"/"+str(agp), temp_image_path+"/"+"agp.tiff")

    mito = sheet.loc[i, 'mito']
    print("MITO")
    print(mito)
    shutil.copy(image_path+"/"+str(mito), temp_image_path)
    os.rename(temp_image_path+"/"+str(mito), temp_image_path+"/"+"mito.tiff")

    treatment = sheet.loc[i, 'treatment']
    print(treatment)
    with open(target_name_path, 'w') as file:
        file.write(str(treatment))
    file.close()







def main(args):
    # meta = pd.read_csv("/eagle/projects/FoundEpidem/astroka/top_ten_100_each_metadata.csv")
    # meta = pd.read_csv("/eagle/projects/FoundEpidem/astroka/linked_metadata.csv")

    temp_image_path =  "/home/astroka/workspace/JUMP_vision_model/rad_pipeline/image_temp"
    target_name_path =  "/home/astroka/workspace/JUMP_vision_model/rad_pipeline/target_name.txt"
    # segmented_image_path = "/eagle/projects/FoundEpidem/astroka/top_10/segmented_images"
    segmented_image_path = "/eagle/projects/FoundEpidem/astroka/pilot_imgs/segmented_images"

    if os.path.isdir(temp_image_path) == False:
        os.mkdir(temp_image_path)
    
    index = vars(args)["index"]
    image_path = vars(args)["path"]
    pull_image(index, image_path, temp_image_path, target_name_path)
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


    args = parser.parse_args()

    main(args)