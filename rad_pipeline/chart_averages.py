import os
import pandas as pd

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
                        print(f"Processed: {file}, Average Intensity: {avg_intensity}")
                    else:
                        print(f"Column 'Intensity_MedianIntensity_RescaleER' not found in {file}")
                except Exception as e:
                    print(f"Error processing {file}: {e}")
    
    return averages, labels

repo1_averages, repo1_labels = extract_intensity_averages("/eagle/projects/FoundEpidem/astroka/rpe/week_one/ind_channels_seg/ch6/csv_files_2.0")
repo2_averages, repo2_labels = extract_intensity_averages("/eagle/projects/FoundEpidem/astroka/rpe/week_nine/ind_channels_seg/ch6/csv_files_2.0")

print("AVG1", repo1_averages)
print(" ")
print("LABELS1", repo1_labels)
print(" ")
print("AVG2", repo2_averages)
print(" ")
print("LABELS2", repo2_labels)