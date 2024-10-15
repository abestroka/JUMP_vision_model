import pandas as pd
import os
import random
import string
import shutil
import argparse
import numpy as np

all_sum = None
num_files = 0 

def generate_graph(src_dir):
    images = os.listdir(src_dir)

    for image in images:
        if "data" in image: #new data found
            curr_path = os.path.join(src_dir, image)
            df = pd.read_csv(curr_path)
            row = df.iloc[0]
            print(row)

            if all_sum is None:
                all_sum = row
            else:
                all_sum += row
            
            num_files += 1
        
        if num_files == 10:
            break
    
    average_row = all_sum/num_files
    average_df = pd.DataFrame([average_row])
    print(average_df)







def main(args):

    src_dir = vars(args)["source"]


    if __name__ == "__main__":
        parser = argparse.ArgumentParser()

        parser.add_argument(
        "-s",
        "--source",
        help="source folder name",
        type=str,
        required=True,
        )