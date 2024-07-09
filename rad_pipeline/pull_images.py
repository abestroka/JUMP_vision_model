import pandas as pd
import os
import random
import string
import shutil
import argparse
import numpy as np

# import path


def pull_image(i, image_path, temp_image_path):

    # sheet_path =  image_path[:-6]+"all_images.xlsx"
    sheet_path = image_path
    print(sheet_path)
    sheet = pd.read_excel(sheet_path)


    dna = sheet.loc[i, 'dna']
    print("DNA")
    print(dna)
    shutil.copy(image_path+str(dna), temp_image_path)
    # TODO: RENAME?

    rna = sheet.loc[i, 'rna']
    print("RNA")
    print(rna)
    shutil.copy(image_path+str(rna), temp_image_path)

    er = sheet.loc[i, 'er']
    print("ER")
    print(er)
    shutil.copy(image_path+str(er), temp_image_path)

    agp = sheet.loc[i, 'agp']
    print("AGP")
    print(agp)
    shutil.copy(image_path+str(agp), temp_image_path)

    mito = sheet.loc[i, 'mito']
    print("MITO")
    print(mito)
    shutil.copy(image_path+str(mito), temp_image_path)

    # dna_path = linked["PathName_OrigDNA"][i]
    # dna_file = linked["FileName_OrigDNA"][i]
    # dna_key = dna_path+dna_file
    # dna_key = dna_key[26:]

    # er_path = linked["PathName_OrigER"][i]
    # er_file = linked["FileName_OrigER"][i]
    # er_key = er_path+er_file
    # er_key = er_key[26:]

    # rna_path = linked["PathName_OrigRNA"][i]
    # rna_file = linked["FileName_OrigRNA"][i]
    # rna_key = rna_path+rna_file
    # rna_key = rna_key[26:]

    # agp_path = linked["PathName_OrigAGP"][i]
    # agp_file = linked["FileName_OrigAGP"][i]
    # agp_key = agp_path+agp_file
    # agp_key = agp_key[26:]

    # mito_path = linked["PathName_OrigMito"][i]
    # mito_file = linked["FileName_OrigMito"][i]
    # mito_key = mito_path+mito_file
    # mito_key = mito_key[26:]


    # illum_dna_path = linked["PathName_IllumDNA"][i]
    # illum_dna_file = linked["FileName_IllumDNA"][i]
    # illum_dna_key = illum_dna_path+"/"+illum_dna_file
    # illum_dna_key = illum_dna_key[26:]

    # illum_er_path = linked["PathName_IllumER"][i]
    # illum_er_file = linked["FileName_IllumER"][i]
    # illum_er_key = illum_er_path+"/"+illum_er_file
    # illum_er_key = illum_er_key[26:]

    # illum_rna_path = linked["PathName_IllumRNA"][i]
    # illum_rna_file = linked["FileName_IllumRNA"][i]
    # illum_rna_key = illum_rna_path+"/"+illum_rna_file
    # illum_rna_key = illum_rna_key[26:]

    # illum_agp_path = linked["PathName_IllumAGP"][i]
    # illum_agp_file = linked["FileName_IllumAGP"][i]
    # illum_agp_key = illum_agp_path+"/"+illum_agp_file
    # illum_agp_key = illum_agp_key[26:]

    # illum_mito_path = linked["PathName_IllumMito"][i]
    # illum_mito_file = linked["FileName_IllumMito"][i]
    # illum_mito_key = illum_mito_path+"/"+illum_mito_file
    # illum_mito_key = illum_mito_key[26:]

    # target = linked["Metadata_InChIKey"][i]
    
    # f = open('/home/astroka/workspace/JUMP_vision_model/target_name.txt', 'w')
    # f.truncate(0)
    # f.write(target)
    # f.close()





def main(args):
    # meta = pd.read_csv("/eagle/projects/FoundEpidem/astroka/top_ten_100_each_metadata.csv")
    # meta = pd.read_csv("/eagle/projects/FoundEpidem/astroka/linked_metadata.csv")

    temp_image_path =  "/home/astroka/workspace/JUMP_vision_model/rad_pipeline/image_temp"
    # segmented_image_path = "/eagle/projects/FoundEpidem/astroka/top_10/segmented_images"
    segmented_image_path = "/eagle/projects/FoundEpidem/astroka/pilot_imgs/segmented_images"

    if os.path.isdir(temp_image_path) == False:
        os.mkdir(temp_image_path)
    index = vars(args)["index"]
    image_path = vars(args)["path"]
    pull_image(index, image_path, temp_image_path)
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