# import os
# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np


# def extract_intensity_averages(repo_path):
#     """
#     Extracts the average of the 'Intensity_MedianIntensity_RescaleER' column
#     from all CSV files in a given repository.
    
#     :param repo_path: Path to the repository
#     :return: A tuple of two lists - (averages, labels)
#     """
#     averages = []
#     labels = []
    
#     if not os.path.exists(repo_path):
#         print(f"Repository path {repo_path} does not exist.")
#         return averages, labels
    
#     # Walk through the repository and find CSV files
#     for root, _, files in os.walk(repo_path):
#         for file in files:
#             if file.endswith(".csv"):
#                 file_path = os.path.join(root, file)
                
#                 try:
#                     df = pd.read_csv(file_path)
#                     if 'Intensity_MedianIntensity_RescaleER' in df.columns:
#                         avg_intensity = df['Intensity_MedianIntensity_RescaleER'].mean()
#                         averages.append(avg_intensity)
#                         labels.append(file.split('.')[0])  # Extract filename without extension
#                         # print(f"Processed: {file}, Average Intensity: {avg_intensity}")
#                     else:
#                         print(f"Column 'Intensity_MedianIntensity_RescaleER' not found in {file}")
#                 except Exception as e:
#                     print(f"Error processing {file}: {e}")
    
#     return averages, labels



# # def plot_comparison(repo1_averages, repo2_averages, labels, save_path):
# #     """
# #     Plots a bar graph comparing the intensity averages from two repositories and saves it.
    
# #     :param repo1_averages: List of average intensities from repository 1
# #     :param repo2_averages: List of average intensities from repository 2
# #     :param labels: List of labels corresponding to each file
# #     :param save_path: Path to save the output plot
# #     """
# #     x = range(len(labels))
# #     width = 0.4  # Bar width
    
# #     plt.figure(figsize=(12, 6))
# #     plt.bar([i - width/2 for i in x], repo1_averages, width=width, label='Week 1')
# #     plt.bar([i + width/2 for i in x], repo2_averages, width=width, label='Week 9')
    
# #     plt.xticks(x, labels, rotation=90)
# #     plt.xlabel("Locations")
# #     plt.ylabel("Average Intensity")
# #     plt.title("Weeks 1 vs 9 2.0 Dose Average Median Ch6 Intensity Per Field")
# #     plt.legend()
# #     plt.tight_layout()
# #     plt.savefig(save_path)
# #     plt.close()
# #     print(f"Plot saved to {save_path}")

# def plot_comparison(repo1_averages, repo2_averages, labels, save_path):
#     """
#     Plots a line graph comparing the intensity averages from two repositories and saves it.
    
#     :param repo1_averages: List of average intensities from repository 1
#     :param repo2_averages: List of average intensities from repository 2
#     :param labels: List of labels corresponding to each file
#     :param save_path: Path to save the output plot
#     """
#     x = range(len(labels))
    
#     plt.figure(figsize=(12, 6))
#     plt.plot(x, repo1_averages, marker='o', linestyle='-', label='Week 1')
#     plt.plot(x, repo2_averages, marker='s', linestyle='-', label='Week 9')

#     avg1 = np.mean(repo1_averages)
#     avg2 = np.mean(repo2_averages)
#     print("WEEK 1 AVG:", avg1)
#     print("WEEK 9 AVG:", avg2)
#     plt.axhline(y=avg1, color='r', linestyle='--', label='Week 1 Average')
#     plt.axhline(y=avg2, color='b', linestyle='--', label='Week 9 Average')

    
#     plt.xlabel("Well Location")
#     plt.ylabel("Average Intensity")
#     plt.title("Weeks 1 vs 9 2.0 Dose Average Median Ch6 Intensity Per Field")
#     plt.legend()
#     plt.tight_layout()
#     plt.savefig(save_path)
#     plt.close()
#     # print(f"Plot saved to {save_path}")

# repo1_averages, repo1_labels = extract_intensity_averages("/eagle/projects/FoundEpidem/astroka/rpe/week_one/ind_channels_seg/ch6/csv_files_2.0")
# repo2_averages, repo2_labels = extract_intensity_averages("/eagle/projects/FoundEpidem/astroka/rpe/week_nine/ind_channels_seg/ch6/csv_files_2.0")

# if repo1_labels == repo2_labels:
#     plot_comparison(repo1_averages, repo2_averages, repo1_labels, "/eagle/projects/FoundEpidem/astroka/rpe/week_one/week1_vs_9_2.0_ch6_line.png")
# else:
#     print("Labels do not match between repositories.")
#     plot_comparison(repo1_averages, repo2_averages, repo1_labels, "/eagle/projects/FoundEpidem/astroka/rpe/week_one/week1_vs_9_2.0_ch6_line.png")


import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def extract_intensity_averages(repo_path):
    """
    Extracts the average of the 'Intensity_MedianIntensity_RescaleER' column
    from all CSV files in a given repository.
    
    :param repo_path: Path to the repository
    :return: A tuple of two lists - (averages, labels)
    """
    averages = []
    labels = []
    
    if not os.path.exists(repo_path):
        print(f"Repository path {repo_path} does not exist.")
        return averages, labels
    
    # Walk through the repository and find CSV files
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)
                
                try:
                    df = pd.read_csv(file_path)
                    if 'Intensity_MedianIntensity_RescaleER' in df.columns:
                        avg_intensity = df['Intensity_MedianIntensity_RescaleER'].mean()
                        averages.append(avg_intensity)
                        labels.append(file.split('.')[0])  # Extract filename without extension
                        # print(f"Processed: {file}, Average Intensity: {avg_intensity}")
                    else:
                        print(f"Column 'Intensity_MedianIntensity_RescaleER' not found in {file}")
                except Exception as e:
                    print(f"Error processing {file}: {e}")
    
    return averages, labels



# def plot_comparison(repo1_averages, repo2_averages, labels, save_path):
#     """
#     Plots a bar graph comparing the intensity averages from two repositories and saves it.
    
#     :param repo1_averages: List of average intensities from repository 1
#     :param repo2_averages: List of average intensities from repository 2
#     :param labels: List of labels corresponding to each file
#     :param save_path: Path to save the output plot
#     """
#     x = range(len(labels))
#     width = 0.4  # Bar width
    
#     plt.figure(figsize=(12, 6))
#     plt.bar([i - width/2 for i in x], repo1_averages, width=width, label='Week 1')
#     plt.bar([i + width/2 for i in x], repo2_averages, width=width, label='Week 9')
    
#     plt.xticks(x, labels, rotation=90)
#     plt.xlabel("Locations")
#     plt.ylabel("Average Intensity")
#     plt.title("Weeks 1 vs 9 2.0 Dose Average Median Ch6 Intensity Per Field")
#     plt.legend()
#     plt.tight_layout()
#     plt.savefig(save_path)
#     plt.close()
#     print(f"Plot saved to {save_path}")

def plot_comparison(repo1_averages, repo2_averages, labels, save_path):
    """
    Plots a line graph comparing the intensity averages from two repositories and saves it.
    
    :param repo1_averages: List of average intensities from repository 1
    :param repo2_averages: List of average intensities from repository 2
    :param labels: List of labels corresponding to each file
    :param save_path: Path to save the output plot
    """
    x = range(len(labels))
    
    plt.figure(figsize=(12, 6))
    plt.plot(x, repo1_averages, marker='o', linestyle='-', label='DMSO')
    plt.plot(x, repo2_averages, marker='s', linestyle='-', label='Compound 4')

    avg1 = np.mean(repo1_averages)
    avg2 = np.mean(repo2_averages)
    print("DMSO AVG:", avg1)
    print("Compound AVG:", avg2)
    plt.axhline(y=avg1, color='r', linestyle='--', label='DMSO Average')
    plt.axhline(y=avg2, color='b', linestyle='--', label='Compound 4 Average')

    
    plt.xlabel("Well Location")
    plt.ylabel("Average Intensity")
    plt.title("DMSO vs Compound 4 Average Median Ch6 Intensity Per Field")
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    # print(f"Plot saved to {save_path}")

repo1_averages, repo1_labels = extract_intensity_averages("/eagle/projects/FoundEpidem/astroka/rpe/week_one/ind_channels_seg_control/ch6/csv_files_Compound_1")
repo2_averages, repo2_labels = extract_intensity_averages("/eagle/projects/FoundEpidem/astroka/rpe/week_one/ind_channels_seg_control/ch6/csv_files_Compound_4")

if repo1_labels == repo2_labels:
    plot_comparison(repo1_averages, repo2_averages, repo1_labels, "/eagle/projects/FoundEpidem/astroka/rpe/week_one/week_1_compounds_1_vs_4_ch6_line.png")
else:
    print("Labels do not match between repositories.")
    plot_comparison(repo1_averages, repo2_averages, repo1_labels, "/eagle/projects/FoundEpidem/astroka/rpe/week_one/week_1_compounds_1_vs_4_ch6_line.png")
