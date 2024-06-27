import pandas as pd
import os
import random
import string
import shutil
import argparse
import numpy as np
# import path


def pull_image(i, image_path, temp_image_path, plate):

    treatment_file = '/home/astroka/workspace/JUMP_vision_model/target_name.txt'
    treatments = pd.read_excel(treatment_file, sheet_name=plate)

    for index, row in treatments.iterrows():
        location = row['Location']
        treatment = row['Treatment']

        # pull the every image set at this location
        well_images = [file for file in image_path if location in file]

        #iterate through, first by field, then by stack

        #iterate through fields
        for field in range(9):
            for stack in range(5):
                curr_images = [file for file in well_images if "f0"+field in file and "p0"+stack in file]


                f = open('/home/astroka/workspace/JUMP_vision_model/target_name.txt', 'w')
                f.truncate(0)
                f.write(treatment)
                f.close()






    # seg_image_path = "/eagle/projects/APSDataAnalysis/LUCID/segmented_images/" + str(i)
    # print('seg image path')
    # print(seg_image_path)

    # if os.path.isdir(seg_image_path) == False:
    #     os.mkdir(seg_image_path)
    #     print('seg_image_path created')

    # base_path = "/eagle/projects/APSDataAnalysis/LUCID"
    # path.mkdirs(temp_image_path)
    curr_path = temp_image_path

    s3.download_file('cellpainting-gallery', dna_key, curr_path+ "/dna.tiff")
    s3.download_file('cellpainting-gallery', er_key, curr_path+ "/er.tiff")
    s3.download_file('cellpainting-gallery', rna_key, curr_path+ "/rna.tiff")
    s3.download_file('cellpainting-gallery', agp_key, curr_path+ "/agp.tiff")
    s3.download_file('cellpainting-gallery', mito_key, curr_path+ "/mito.tiff")
    s3.download_file('cellpainting-gallery', illum_dna_key, curr_path+ "/illum_dna.npy")
    s3.download_file('cellpainting-gallery', illum_er_key, curr_path+ "/illum_er.npy")
    s3.download_file('cellpainting-gallery', illum_rna_key, curr_path+ "/illum_rna.npy")
    s3.download_file('cellpainting-gallery', illum_agp_key, curr_path+ "/illum_agp.npy")
    s3.download_file('cellpainting-gallery', illum_mito_key, curr_path+ "/illum_mito.npy")






def main(args):
    # meta = pd.read_csv("/eagle/projects/FoundEpidem/astroka/top_ten_100_each_metadata.csv")
    meta = pd.read_csv("/eagle/projects/FoundEpidem/astroka/linked_metadata.csv")

    temp_image_path =  "/home/astroka/workspace/JUMP_vision_model/image_temp"
    # segmented_image_path = "/eagle/projects/FoundEpidem/astroka/top_10/segmented_images"
    segmented_image_path = "/eagle/projects/FoundEpidem/astroka/segmented_images"

    if os.path.isdir(temp_image_path) == False:
        os.mkdir(temp_image_path)
    index = vars(args)["index"]
    pull_image(index, meta, temp_image_path)
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


    args = parser.parse_args()

    main(args)