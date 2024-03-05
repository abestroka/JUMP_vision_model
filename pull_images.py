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


def pull_image(i, linked, temp_image_path):
    s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))





    dna_path = linked["PathName_OrigDNA"][i]
    dna_file = linked["FileName_OrigDNA"][i]
    dna_key = dna_path+dna_file
    dna_key = dna_key[26:]

    er_path = linked["PathName_OrigER"][i]
    er_file = linked["FileName_OrigER"][i]
    er_key = er_path+er_file
    er_key = er_key[26:]

    rna_path = linked["PathName_OrigRNA"][i]
    rna_file = linked["FileName_OrigRNA"][i]
    rna_key = rna_path+rna_file
    rna_key = rna_key[26:]

    agp_path = linked["PathName_OrigAGP"][i]
    agp_file = linked["FileName_OrigAGP"][i]
    agp_key = agp_path+agp_file
    agp_key = agp_key[26:]

    mito_path = linked["PathName_OrigMito"][i]
    mito_file = linked["FileName_OrigMito"][i]
    mito_key = mito_path+mito_file
    mito_key = mito_key[26:]


    illum_dna_path = linked["PathName_IllumDNA"][i]
    illum_dna_file = linked["FileName_IllumDNA"][i]
    illum_dna_key = illum_dna_path+illum_dna_file
    illum_dna_key = illum_dna_key[26:]

    illum_er_path = linked["PathName_IllumER"][i]
    illum_er_file = linked["FileName_IllumER"][i]
    illum_er_key = illum_er_path+illum_er_file
    illum_er_key = illum_er_key[26:]

    illum_rna_path = linked["PathName_IllumRNA"][i]
    illum_rna_file = linked["FileName_IllumRNA"][i]
    illum_rna_key = illum_rna_path+illum_rna_file
    illum_rna_key = illum_rna_key[26:]

    illum_agp_path = linked["PathName_IllumAGP"][i]
    illum_agp_file = linked["FileName_IllumAGP"][i]
    illum_agp_key = illum_agp_path+illum_agp_file
    illum_agp_key = illum_agp_key[26:]

    illum_mito_path = linked["PathName_IllumMito"][i]
    illum_mito_file = linked["FileName_IllumMito"][i]
    illum_mito_key = illum_mito_path+illum_mito_file
    illum_mito_key = illum_mito_key[26:]

    target = linked["Metadata_InChIKey"][i]

    print('DNA KEY')
    print(dna_key)

    print('TEMP IMAGE PATH')
    print(temp_image_path)

    print("FULL PATH")
    print(temp_image_path+ "/dna.tiff")

    s3.download_file('cellpainting-gallery', dna_key, temp_image_path+ "/dna.tiff")
    s3.download_file('cellpainting-gallery', er_key, temp_image_path+ "/er.tiff")
    s3.download_file('cellpainting-gallery', rna_key, temp_image_path+ "/rna.tiff")
    s3.download_file('cellpainting-gallery', agp_key, temp_image_path+ "/agp.tiff")
    s3.download_file('cellpainting-gallery', mito_key, temp_image_path+ "/mito.tiff")
    s3.download_file('cellpainting-gallery', illum_dna_key, temp_image_path+ "/illum_dna.npy")
    s3.download_file('cellpainting-gallery', illum_er_key, temp_image_path+ "/illum_er.npy")
    s3.download_file('cellpainting-gallery', illum_rna_key, temp_image_path+ "/illum_rna.npy")
    s3.download_file('cellpainting-gallery', illum_agp_key, temp_image_path+ "/illum_agp.npy")
    s3.download_file('cellpainting-gallery', illum_mito_key, temp_image_path+ "/illum_mito.npy")






def main(index):
    meta = pd.read_csv('~/workspace/JUMP_vision_model/linked_metadata.csv')
    print(meta)
    temp_image_path = "~/workspace/JUMP_vision_model/image_temp"
    pull_image(1, meta, temp_image_path)

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

    print("ARGS")
    print(args)

    main(args)