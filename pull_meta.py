import pandas as pd
import os
import random
import string
import shutil
import argparse
import numpy as np

def pull_meta(num_samples):
    profile_formatter = (
    "s3://cellpainting-gallery/cpg0016-jump/"
    "{Metadata_Source}/workspace/profiles/"
    "{Metadata_Batch}/{Metadata_Plate}/{Metadata_Plate}.parquet"
)
    loaddata_formatter = (
    "s3://cellpainting-gallery/cpg0016-jump/"
    "{Metadata_Source}/workspace/load_data_csv/"
    "{Metadata_Batch}/{Metadata_Plate}/load_data_with_illum.parquet"
)
    
    plates = pd.read_csv("~/workspace/JUMP_vision_model/datasets/metadata/plate.csv.gz")
    wells = pd.read_csv("~/workspace/JUMP_vision_model/datasets/metadata/well.csv.gz")
    compound = pd.read_csv("~/workspace/JUMP_vision_model/datasets/metadata/compound.csv.gz")
    orf = pd.read_csv("~/workspace/JUMP_vision_model/datasets/metadata/orf.csv.gz")

    #get all plates treated with compound
    # sample = (
    # plates.query('Metadata_PlateType=="COMPOUND"')
    # )

    sample = (
        plates.query('Metadata_PlateType=="COMPOUND"')
)
    # idx = np.random.choice(len(sample1)-1, replace=True, size=num_samples)
    # sample = sample1.iloc[idx]
    # sample = sample.sample(n=num_samples)
    # sample = plates

    # load profiles of all plates
    dframes = []
    i = 0
    u = len(sample)
    # columns = ["Cells_AreaShape_Exent"]
    # # ["Count"]
    columns = [
        "Metadata_Source",
        "Metadata_Plate",
        "Metadata_Well",
    ]
    for _, row in sample.iterrows():
        s3_path = profile_formatter.format(**row.to_dict())
        dframes.append(
            pd.read_parquet(s3_path, storage_options={"anon": True}, columns=columns)
        )
        i+=1
        print("profile " + str(i) + " of " + str(u) + " complete")
        
    dframes = pd.concat(dframes)

    # merge compounds and wells, then merge all metadata to plates list (dframes)
    metadata = compound.merge(wells, on="Metadata_JCP2022")
    ann_dframe = metadata.merge(
        dframes, on=["Metadata_Source", "Metadata_Plate", "Metadata_Well"]
    )

    load_data = []
    i = 0
    u = len(sample)
    for _, row in sample.iterrows():
        s3_path = loaddata_formatter.format(**row.to_dict())
        load_data.append(pd.read_parquet(s3_path, storage_options={"anon": True}))
        i+=1
        print("profile " + str(i) + " of " + str(u) + " complete")

    load_data = pd.concat(load_data)

    # link metadata with image filepaths
    linked = pd.merge(
        load_data, ann_dframe, on=["Metadata_Source", "Metadata_Plate", "Metadata_Well"]
    )

    linked.to_csv('~/workspace/JUMP_vision_model/linked_metadata.csv', index=False)
    
    return linked

def create_dir(target):
    cells_path = "/workspace/results/segmented_image_temp"
    dst_dir = os.path.join(cells_path, target)
    exists = os.path.exists(dst_dir)
    if exists == False:
        os.mkdir(dst_dir) 
    
def temp_to_dst(target):
    cells_path = "/workspace/results/segmented_image_temp"
    dst_dir = os.path.join(cells_path, target)
    src_dir = os.path.join(cells_path, "temp")

    dst_images = os.listdir(dst_dir)
    src_images = os.listdir(src_dir)

    for image in src_images:
        curr_path = os.path.join(src_dir, image)
    #         if image in dst_images:
        # rename so no overwrite
        new_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))
        new_name = new_name + ".png"
        new_path = os.path.join(src_dir, new_name)
        os.rename(curr_path, new_path)

        #transfer image
        shutil.copy(new_path, dst_dir)
    
    # delete temp directory
    shutil.rmtree(src_dir)




def find_treatment(s3path):
    meta = pull_meta()
    treatment = meta.query('PathName_OrigDNA=="{s3path}"')["Metadata_InChIKey"]

    return treatment

def pull_image(i, linked):
    for _, row in linked.iterrows():
        dna_path = linked["PathName_OrigDNA"][i]
        dna_file = linked["FileName_OrigDNA"][i]
        er_path = linked["PathName_OrigER"][i]
        er_file = linked["FileName_OrigER"][i]
        rna_path = linked["PathName_OrigRNA"][i]
        rna_file = linked["FileName_OrigRNA"][i]
        agp_path = linked["PathName_OrigAGP"][i]
        agp_file = linked["FileName_OrigAGP"][i]
        mito_path = linked["PathName_OrigMito"][i]
        mito_file = linked["FileName_OrigMito"][i]

        illum_dna_path = linked["PathName_IllumDNA"][i]
        illum_dna_file = linked["FileName_IllumDNA"][i]
        illum_er_path = linked["PathName_IllumER"][i]
        illum_er_file = linked["FileName_IllumER"][i]
        illum_rna_path = linked["PathName_IllumRNA"][i]
        illum_rna_file = linked["FileName_IllumRNA"][i]
        illum_agp_path = linked["PathName_IllumAGP"][i]
        illum_agp_file = linked["FileName_IllumAGP"][i]
        illum_mito_path = linked["PathName_IllumMito"][i]
        illum_mito_file = linked["FileName_IllumMito"][i]

        target = linked["Metadata_InChIKey"][i]

    

def main(num_samples, num_image_sets):
    meta = pull_meta(num_samples)
    temp_image_path = "~/workspace/JUMP_vision_model/image_temp"
    for i in range(num_image_sets):
        pull_image(i, meta)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
    "-s",
    "--num_samples",
    help="number of samples to be taken from metadata",
    type=int,
    required=True,
    )
    # parser.add_argument(
    # "-i",
    # "--num_image_sets",
    # help="number of image sets to be pulled from metadata",
    # type=int,
    # required=True,
    # )

    args = parser.parse_args()

    main(args)