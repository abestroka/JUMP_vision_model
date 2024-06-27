import pandas as pd
import os
import random
import string
import shutil
import argparse
import numpy as np



def pull_image(image_path, plate):

    columns = ['index', 'dna' 'rna', 'agp', 'er', 'mito', 'brightfield', 'treatment']
    all_imgs = pd.DataFrame(columns=columns)

    treatment_file = '/home/astroka/workspace/JUMP_vision_model/rad_pipeline/pilot_cells_layout.xlsx'
    treatments = pd.read_excel(treatment_file, sheet_name=plate)
    print("TREATMENTS")
    print(treatments)
    p = 1
    for index, row in treatments.iterrows():
        location = row['Location']
        treatment = row['Treatment']
        print('LOCATION')
        print(location)
        # pull the every image set at this location
        well_images = []
        # well_images = [file for file in image_path if location in file]
        for file in os.listdir(image_path):
            if str(location) in str(file):
                well_images.append(file)



        #iterate through, first by field, then by stack

        print("WELL IMAGES")
        print(well_images)

        #iterate through fields
        for field in range(9):
            for stack in range(5):
                curr_images = [file for file in well_images if "f0"+str(field) in file and "p0"+str(stack) in file]
                print("CURRENT IMAGES")
                print(curr_images)
                # all_imgs[p, 'index'] = p
                #iterate through images of this set
                # dna = 'NA'
                # rna = 'NA'
                # agp = 'NA'
                # er = 'NA'
                # brightfield = 'NA'
                # mito = 'NA'
                for img in curr_images:
                    print("IMAGE")
                    print(img)
                    if 'ch2' in img:
                        dna = img
                    elif 'ch4' in img:
                        rna = img
                    elif 'ch3' in img:
                        agp = img
                    elif 'ch6' in img:
                        er = img
                    elif 'ch7' in img:
                        brightfield = img
                    elif 'ch8' in img:
                        mito = img
                print(p)
                new_row = {'index': str(p), 'dna': str(dna), 'rna': str(rna), 'agp': str(agp), 'er': str(er), 'mito': str(mito), 'brightfield': str(brightfield), 'treatment': str(treatment)}
                new_row_df = pd.DataFrame([new_row])
                all_imgs = pd.concat([all_imgs, new_row_df], ignore_index=True)
                p+=1

    export_path = image_path[:-6]+"all_images.xlsx"
    # export_path = "/eagle/FoundEpidem/astroka/pilot_imgs/Test1/20240517_OSU_HTSC_MW_ANL_CellPainting_P3_2__2024-05-17T15_59_05-Measurement 1/all_images.xlsx"
    all_imgs.to_excel(export_path, index=False)

    num_rows = all_imgs.shape[0]
    f = open('/home/astroka/workspace/JUMP_vision_model/rad_pipeline/num_images.txt', 'w')
    f.truncate(0)
    f.write(str(num_rows))
    f.close()



def main(args):
    path = vars(args)["image_path"]
    plate = vars(args)["plate"]
    pull_image(path, plate)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
    "-i",
    "--image_path",
    help="path to find cell images",
    type=str,
    required=True,
    )
    parser.add_argument(
    "-p",
    "--plate",
    help="plate number",
    type=str,
    required=True,
    )


    args = parser.parse_args()

    main(args)