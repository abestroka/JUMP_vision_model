import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from statistics import mean

repo_path = "/eagle/projects/FoundEpidem/astroka/rpe/"

nuclei_size_avgs = []
doses = ["0.001", "0.01", "0.1", "1.0", "2.0"]
type = "rpe_rad"
results = {dose: [] for dose in doses}

week_folders = [f for f in os.listdir(repo_path) if f.startswith("week_")]

for week in week_folders:
    week_path = os.path.join(repo_path, week, "sheets", "rpe_rad")
    if not os.path.isdir(week_path):
        continue

    week_vals = []

    for dose in doses:
        dose_path = os.path.join(week_path, dose)
        if not os.path.isdir(dose_path):
            results[dose].append(np.nan)
            continue
        
        values = []
        for file in os.listdir(dose_path):
            if file.endswith("nuclei.csv"):
                df = pd.read_csv(os.path.join(dose_path, file))
                col_data = df["AreaShape_Area"].tolist()
                # print("RAD", col_data)
                if col_data != []:

                    values.append(mean(col_data))
        
        week_vals.append(values)

################

    dose_path = os.path.join(repo_path, week, "sheets", "rpe_control", "untreated")
        
    values = []
    for file in os.listdir(dose_path):
        if file.endswith("nuclei.csv"):
            df = pd.read_csv(os.path.join(dose_path, file))
            col_data = df["AreaShape_Area"].tolist()
            # print("UNTREATED", col_data)
            if col_data != []:
                values.append(mean(col_data))
    week_vals.append(values)

    nuclei_size_avgs.append(week_vals)

# for week in week_folders:
#     week_path = os.path.join(repo_path, week, "sheets", "rpe_control")
#     if not os.path.isdir(week_path):
#         continue

#     week_vals = []

#     dose_path = os.path.join(week_path, "untreated")
        
#     values = []
#     for file in os.listdir(dose_path):
#         if file.endswith("nuclei.csv"):
#             df = pd.read_csv(os.path.join(dose_path, file))
#             col_data = df["AreaShape_Area"].tolist()
#             # print("UNTREATED", col_data)
#             if col_data != []:
#                 values.append(mean(col_data))
        
#     week_vals.append(values)

# nuclei_size_avgs.append(week_vals)


doses.append("untreated")




colors = plt.cm.tab10.colors[:6]
fig, ax = plt.subplots(figsize=(10, 6))
for i in range(9):  # x-axis categories
    for j in range(6):  # 5 groups per category
        # spread out the x values a little so they don't overlap
        x_vals = np.full(180, i) + (j - 2) * 0.1  
        y_vals = nuclei_size_avgs[i, j, :]
        ax.scatter(x_vals, y_vals, color=colors[j], alpha=0.6, s=10, label=f"Group {j+1}" if i == 0 else "")

ax.set_xticks(range(9))
ax.set_xticklabels(doses)
ax.set_xlabel("Categories (10)")
ax.set_ylabel("Values (180 per group)")
ax.legend(title="Groups (5)")
# plt.show()

repo_path = "/eagle/projects/FoundEpidem/astroka/ten_week/"

png_path = os.path.join(repo_path, "average_nuclei_size.png")
plt.savefig(png_path, dpi=300)
plt.close()

# print(nuclei_size_avgs)
# print(len(nuclei_size_avgs))
# print(len(nuclei_size_avgs[0]))
# print(len(nuclei_size_avgs[0][0]))
# print(" ")
# # print(nuclei_size_avgs.shape())

# plt.boxplot(nuclei_size_avgs, labels=doses)

# plt.ylabel("Nuclei Size")
# plt.xlabel("Dose")
# plt.title("Huvec Nuclei Size")

# repo_path = "/eagle/projects/FoundEpidem/astroka/ten_week/"

# png_path = os.path.join(repo_path, "average_nuclei_size.png")
# plt.savefig(png_path, dpi=300)
# plt.close()
