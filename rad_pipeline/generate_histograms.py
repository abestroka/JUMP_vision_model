import pandas as pd
import os
import random
import string
import shutil
import argparse
import numpy as np
import matplotlib.pyplot as plt


def generate_graph(src_dir):
    all_sum = None
    num_files = 0 
    # images = os.listdir(src_dir)
    to_remove = ['ImageNumber', 'ObjectNumber']
    average_df = pd.DataFrame()

    treatments = ['untreated', 'Compound_1', 'Compound_2', 'Compound_3', 'Compound_4', 'Compound_5', 'Compound_6', 'Compound_7', 'Compound_8', 'Compound_9', 'Compound_10', 'Compound_11', 'Compound_12', 'Compound_13', 'Compound_14', 'Compound_15', 'Compound_16', 'Compound_17']
    for treatment in treatments:
        all_sum = None
        num_files = 0 
        base_dir = src_dir + treatment + '/'
        print("BASE DIR", base_dir)
        images = os.listdir(base_dir)

        for image in images:
            if "data" in image: #new data found
                curr_path = os.path.join(base_dir, image)
                print('CURR_PATH', curr_path)
                df = pd.read_csv(curr_path)
                df = df.drop(columns=to_remove, errors='ignore')
                row = df.iloc[0]
                

                if all_sum is None:
                    all_sum = row
                else:
                    all_sum += row
                
                print("ALL SUM", all_sum)
                
                num_files += 1
            
            if num_files == 10:
                break

        print("ALL SUM 2", all_sum)
        print(num_files)
        average_row = all_sum/num_files
        print("AVG ROW", average_row)
        print("AVG DF", average_df)
        average_row['Treatment'] = treatment
        average_row_df = pd.DataFrame([average_row])
        # average_df = pd.DataFrame([average_row])
        average_df = pd.concat([average_df, average_row_df], ignore_index=True)
        print("FINAL")
        print(average_df)

    average_df.set_index('Treatment', inplace=True)

    # Plotting the bar chart for all treatments' average values
    average_df.T.plot(kind='bar', figsize=(15, 8))  # Transpose to have features on x-axis
    plt.title('Bar Chart of Averages for Each Treatment')
    plt.xlabel('Features')
    plt.ylabel('Average Values')
    plt.xticks(rotation=45, ha='right') # Rotate column labels for better readability


    # Save the histogram to a file
    # output_file = '~/workspace/JUMP_vision_model/rad_pipeline/histogram.png'  # You can change the file name or extension
    # output_file = 'histogram.png'
    output_file = '/eagle/FoundEpidem/astroka/graphs/chart.png'
    # plt.tight_layout()  
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