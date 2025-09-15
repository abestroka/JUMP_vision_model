import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from statistics import mean

repo_path = "/eagle/projects/FoundEpidem/astroka/rpe/"

nuclei_size_avgs = []
doses = ["0.001", "0.01", "0.1", "1.0", "2.0"]
weeks = []
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
                else:
                    print("HERRRE", dose, week)
        
        week_vals.append(values)
    
    weeks.append(week)

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
            else:
                print("HERRRE", dose, week)
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


print(len(nuclei_size_avgs[0]))
print(len(nuclei_size_avgs[1]))
print(len(nuclei_size_avgs[2]))
print(len(nuclei_size_avgs[3]))
print(len(nuclei_size_avgs[4]))
print(len(nuclei_size_avgs[5]))
print(len(nuclei_size_avgs[6]))
print(len(nuclei_size_avgs[7]))
print(len(nuclei_size_avgs[8]))
# print(len(nuclei_size_avgs[0]))

# colors = plt.cm.tab10.colors[:6]

# data = np.array(nuclei_size_avgs)


# colors = plt.cm.tab10.colors[:data.shape[1]]  # 6 distinct colors

colors = plt.cm.tab10.colors[:len(nuclei_size_avgs[0])]

fig, axes = plt.subplots(1, len(nuclei_size_avgs[0]), figsize=(20, 6), sharey=True)
# x_labels = [f"Week {i+1}" for i in range(len(nuclei_size_avgs))]
print(weeks)
x_labels = weeks
# for j in range(len(nuclei_size_avgs[0])):  # 6 groups
    # Collect data for this group: list of 9 arrays, each length 180
    # group_data = [nuclei_size_avgs[i][j] for i in range(len(nuclei_size_avgs))]

for j in range(max(len(row) for row in nuclei_size_avgs)):  # up to max groups
    group_data = [nuclei_size_avgs[i][j] for i in range(len(nuclei_size_avgs)) if j < len(nuclei_size_avgs[i])]
    # now plot group_data

    
    bp = axes[j].boxplot(group_data, patch_artist=True, widths=0.6)
    
    # Color the boxes
    for patch in bp['boxes']:
        patch.set_facecolor(colors[j])
        patch.set_alpha(0.6)
    
    axes[j].set_xticks(range(1, len(nuclei_size_avgs) + 1))
    axes[j].set_xticklabels(x_labels, rotation=45, ha="right")
    axes[j].set_title(doses[j])
    axes[j].set_yscale("log")


axes[0].set_ylabel("Values")
plt.tight_layout()
# plt.show()

repo_path = "/eagle/projects/FoundEpidem/astroka/rpe/"

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
