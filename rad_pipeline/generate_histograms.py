import pandas as pd
import os
import random
import string
import shutil
import argparse
import numpy as np



def generate_graph(src_dir):
    all_sum = None
    num_files = 0 
    images = os.listdir(src_dir)
    to_remove = ['ImageNumber', 'ObjectNumber']

    for image in images:
        if "data" in image: #new data found
            curr_path = os.path.join(src_dir, image)
            df = pd.read_csv(curr_path)
            df = df.drop(columns=to_remove, errors='ignore')
            row = df.iloc[0]
            

            if all_sum is None:
                all_sum = row
            else:
                all_sum += row
            
            num_files += 1
        
        if num_files == 10:
            break
    
    average_row = all_sum/num_files
    average_df = pd.DataFrame([average_row])
    print("FINAL")
    print(average_df)

    # Generate histogram from the values in average_df
    average_values = average_df.iloc[0].values  # Get the values from the DataFrame

    plt.hist(average_values, bins=10, edgecolor='black')
    plt.title('Histogram of Averages')
    plt.xlabel('Values')
    plt.ylabel('Frequency')

    # Save the histogram to a file
    output_file = 'histogram.png'  # You can change the file name or extension
    plt.savefig(output_file)  # Save the plot as an image file
    plt.close() 







def main(args):

    src_dir = vars(args)["source"]
    generate_graph(src_dir)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
    "-s",
    "--source",
    help="source folder name",
    type=str,
    required=True,
    )


    args = parser.parse_args()
    main(args)