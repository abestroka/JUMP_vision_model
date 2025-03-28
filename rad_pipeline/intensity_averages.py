# import os
# import pandas as pd
# import matplotlib.pyplot as plt

# def plot_intensity_averages(base_path, save_path):
#     """
#     Iterates through subdirectories of base_path, finds all CSV files, 
#     computes average 'Intensity_MedianIntensity_RescaleAGP' per CSV,
#     and plots a line graph of these averages per subdirectory.
#     """
#     plt.figure(figsize=(10, 6))

#     for subdir in os.listdir(base_path):
#         subdir_path = os.path.join(base_path, subdir)
#         if os.path.isdir(subdir_path):
#             averages = []
#             filenames = []

#             for file in os.listdir(subdir_path):
#                 if file.endswith('.csv'):
#                     file_path = os.path.join(subdir_path, file)
#                     try:
#                         df = pd.read_csv(file_path)
#                         if 'Intensity_MedianIntensity_RescaleAGP' in df.columns:
#                             avg_value = df['Intensity_MedianIntensity_RescaleAGP'].mean()
#                             averages.append(avg_value)
#                             filenames.append(file)
#                         else:
#                             print(f"Column missing in {file_path}")
#                     except Exception as e:
#                         print(f"Error reading {file_path}: {e}")

#             if averages:
#                 plt.plot(range(len(averages)), averages, label=subdir)

#     plt.title('Average Median Intensity per Treatment')
#     plt.xlabel('')
#     plt.ylabel('Avg Intensity_MedianIntensity_RescaleAGP')
#     plt.legend()
#     plt.grid(True)
#     plt.tight_layout()
#     plt.savefig(save_path)
#     plt.close()

# plot_intensity_averages("/eagle/projects/FoundEpidem/astroka/rpe_2/20x_original/ind_channels_seg/ch3", "/eagle/projects/FoundEpidem/astroka/rpe_2/20x_original/ind_channels_seg/ch3/averages_chart.png")

import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_intensity_boxplot(base_path, save_path):


    data = {}
    
    for subdir in os.listdir(base_path):
        subdir_path = os.path.join(base_path, subdir)
        if os.path.isdir(subdir_path):
            averages = []
            for file in os.listdir(subdir_path):
                if file.endswith('.csv'):
                    file_path = os.path.join(subdir_path, file)
                    try:
                        df = pd.read_csv(file_path)
                        if 'Intensity_UpperQuartileIntensity_RescaleAGP' in df.columns:
                            avg_value = df['Intensity_UpperQuartileIntensity_RescaleAGP'].mean()
                            averages.append(avg_value)
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")
            if averages:
                data[subdir] = averages

    # Plot boxplots
    plt.figure(figsize=(12, 6))
    plt.boxplot(data.values(), labels=data.keys(), showmeans=True)
    plt.xticks(rotation=90)
    plt.title('Distribution of Intensity Averages per Treatment')
    plt.ylabel('Avg Intensity_UpperQuartileIntensity_RescaleAGP')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()




def plot_mean_of_averages_bargraph(base_path, save_path):
    """
    For each subdirectory in base_path:
        - Finds all CSVs
        - Computes the average of 'Intensity_MedianIntensity_RescaleAGP' in each CSV
        - Then computes the mean of those averages per category (subdir)
    Finally, plots a bar graph showing one bar per category.
    """
    category_means = {}

    for subdir in sorted(os.listdir(base_path)):
        subdir_path = os.path.join(base_path, subdir)
        if os.path.isdir(subdir_path):
            csv_averages = []

            for file in os.listdir(subdir_path):
                if file.endswith('.csv'):
                    file_path = os.path.join(subdir_path, file)
                    try:
                        df = pd.read_csv(file_path)
                        if 'Intensity_UpperQuartileIntensity_RescaleAGP' in df.columns:
                            avg = df['Intensity_UpperQuartileIntensity_RescaleAGP'].mean()
                            csv_averages.append(avg)
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")

            if csv_averages:
                category_mean = sum(csv_averages) / len(csv_averages)
                category_means[subdir] = category_mean

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.bar(category_means.keys(), category_means.values(), color='skyblue')
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Mean of Averages')
    plt.title('Upper Quartile Intensity per Treatment')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


plot_intensity_boxplot("/eagle/projects/FoundEpidem/astroka/rpe_2/20x_original/ind_channels_seg/ch3", "/eagle/projects/FoundEpidem/astroka/rpe_2/20x_original/ind_channels_seg/ch3/uq_averages_chart.png")
plot_mean_of_averages_bargraph("/eagle/projects/FoundEpidem/astroka/rpe_2/20x_original/ind_channels_seg/ch3", "/eagle/projects/FoundEpidem/astroka/rpe_2/20x_original/ind_channels_seg/ch3/uq_averages_bar_chart.png")
