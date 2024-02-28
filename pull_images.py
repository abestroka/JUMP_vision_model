import pandas as pd
import os
import random
import string
import shutil
import argparse
import numpy as np


def pull_image(i, linked, temp_image_path):
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


def main(index):
    meta = pd.read_csv('~/workspace/JUMP_vision_model/linked_metadata.csv')
    temp_image_path = "~/workspace/JUMP_vision_model/image_temp"
    pull_image(index, meta, temp_image_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
    "-i",
    "--index",
    help="number of images to be taken from metadata",
    type=int,
    required=True,
    )


    args = parser.parse_args()

    main(args)