import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Path to the repo containing week_* folders
REPO_PATH = "/eagle/projects/FoundEpidem/astroka/rpe/"   # <-- change this to your repo path

# Expected doses
DOSES = ["0.001", "0.01", "0.1", "1", "2"]

# Dictionary to hold results {dose: [week1_avg, week2_avg, ...]}
results = {dose: [] for dose in DOSES}

# Get sorted list of week folders
# week_folders = [f for f in os.listdir(REPO_PATH) if f.startswith("week_")]
import re

def extract_week_number(name):
    match = re.search(r'\d+', name)  # look for digits
    return int(match.group()) if match else float('inf')

# --- sorted list of week folders ---
week_folders = sorted(
    [f for f in os.listdir(REPO_PATH) if f.startswith("week_")],
    key=extract_week_number
)

# numeric week labels for plotting
week_numbers = [extract_week_number(w) for w in week_folders]


for week in week_folders:
    week_path = os.path.join(REPO_PATH, week, "results", "rpe_rad")
    if not os.path.isdir(week_path):
        continue
    
    for dose in DOSES:
        dose_path = os.path.join(week_path, dose)
        if not os.path.isdir(dose_path):
            results[dose].append(np.nan)  # placeholder if missing
            continue
        
        values = []
        for file in os.listdir(dose_path):
            if file.endswith("confluency.txt"):
                with open(os.path.join(dose_path, file), "r") as f:
                    try:
                        values.append(float(f.read().strip()))
                    except ValueError:
                        pass
        
        if values:
            avg_val = np.mean(values)
        else:
            avg_val = np.nan
        results[dose].append(avg_val)

# Convert to DataFrame for easier CSV saving
df = pd.DataFrame(results, index=week_folders)
df.index.name = "Week"

# Save CSV
csv_path = os.path.join(REPO_PATH, "average_confluency.csv")
df.to_csv(csv_path)

# Plotting
plt.figure(figsize=(8, 6))
# weeks = range(1, len(week_folders) + 1)
df = pd.DataFrame(results, index=week_numbers)
df.index.name = "Week"
df.to_csv(csv_path)


for dose, values in results.items():
    plt.plot(week_numbers, values, marker="o", label=f"Dose {dose}")

plt.xticks(week_numbers, week_folders, rotation=45)
plt.xlabel("Week")
plt.ylabel("Average Confluency")
plt.title("Average Confluency per Dose over Weeks")
plt.legend(title="Dose")
plt.grid(True)
plt.tight_layout()

png_path = os.path.join(REPO_PATH, "average_confluency.png")
plt.savefig(png_path, dpi=300)
plt.close()

# for dose, values in results.items():
#     plt.plot(weeks, values, marker="o", label=f"Dose {dose}")

# plt.xticks(weeks, week_folders, rotation=45)
# plt.xlabel("Week")
# plt.ylabel("Average Confluency")
# plt.title("Average Confluency per Dose over Weeks")
# plt.legend(title="Dose")
# plt.grid(True)
# plt.tight_layout()

# # Save graph as PNG
# png_path = os.path.join(REPO_PATH, "average_confluency.png")
# plt.savefig(png_path, dpi=300)
# plt.close()

print(f"Saved results to:\n {csv_path}\n {png_path}")
