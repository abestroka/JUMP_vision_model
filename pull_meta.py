import pandas as pd
import os
import random
import string
import shutil
import argparse
import numpy as np
import boto3
from botocore import UNSIGNED
from botocore.config import Config

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
        # .sample(10, random_state=34)
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

    linked.to_csv("/eagle/projects/FoundEpidem/astroka/linked_metadata.csv", index=False)
    
    return linked

def get_top_ten(linked):
    n = 10
    # linked
    top_ten = linked["Metadata_InChIKey"].value_counts()[:n].index.tolist()
    print("TOP TEN")
    print(top_ten)
    # Filter rows based on whether the specified column contains any of the names in the list
    filtered_df = linked[linked['Metadata_InChiKey'].isin(top_ten)]
    filtered_df.to_csv("/eagle/projects/FoundEpidem/astroka/top_ten_metadata.csv", index=False)

    # Display the filtered DataFrame
    print(filtered_df)



def main(num_samples):
    # meta = pull_meta(num_samples)
    meta = pd.read_csv("/eagle/projects/FoundEpidem/astroka/linked_metadata.csv")

    get_top_ten(meta)
    # temp_image_path = "~/workspace/JUMP_vision_model/image_temp"
    # for i in range(num_image_sets):
    #     pull_image(i, meta, temp_image_path)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
    "-s",
    "--num_samples",
    help="number of samples to be taken from metadata",
    type=int,
    required=True,
    )


    args = parser.parse_args()

    main(args)