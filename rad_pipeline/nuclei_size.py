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


##########

import re

def week_number(label):
    """Extract the week number from a string like 'week_one' -> 1"""
    # If they're written as words like "one", "two" etc
    words_to_nums = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9
    }
    word = label.split("_")[1].lower()
    return words_to_nums[word]

# Pair labels with their data
x_labels = weeks
paired = list(zip(x_labels, nuclei_size_avgs))

# Sort by extracted week number
paired_sorted = sorted(paired, key=lambda x: week_number(x[0]))

# Unpack back into labels and data
x_labels_sorted, nuclei_size_avgs_sorted = zip(*paired_sorted)

# Convert nuclei_size_avgs_sorted back into a list
nuclei_size_avgs_sorted = list(nuclei_size_avgs_sorted)

nuclei_size_avgs = nuclei_size_avgs_sorted
#############

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
    axes[j].set_xticklabels(x_labels_sorted, rotation=45, ha="right")
    axes[j].set_title(doses[j])
    axes[j].set_yscale("log")


axes[0].set_ylabel("Values")
plt.tight_layout()
# plt.show()

repo_path = "/eagle/projects/FoundEpidem/astroka/rpe/"

png_path = os.path.join(repo_path, "average_nuclei_size.png")
plt.savefig(png_path, dpi=300)
plt.close()

# for dose x, does nucleus size change across weeks?

import scipy.stats as stats

p_values = []
for j in range(len(nuclei_size_avgs_sorted[0])):  # loop doses
    # Gather data: 9 groups (weeks), each with replicates
    groups = []
    for i in range(len(nuclei_size_avgs_sorted)):
        if j < len(nuclei_size_avgs_sorted[i]):  # only if this dose exists in that week
            if len(nuclei_size_avgs_sorted[i][j]) > 0:  # skip empty lists
                groups.append(nuclei_size_avgs_sorted[i][j])
    # groups = [nuclei_size_avgs_sorted[i][j] for i in range(len(nuclei_size_avgs_sorted))]
    if len(groups) > 1:
        f_stat, p_val = stats.f_oneway(*groups)
        p_values.append(p_val)
        print(f"Dose {doses[j]}: ANOVA across weeks, p = {p_val:.4e}")
    else:
        print(f"Dose {j+1}: not enough data for ANOVA")


# at week n, does nuclues size differ between doses?
# for i in range(len(nuclei_size_avgs_sorted)):  # loop weeks
#     groups = [nuclei_size_avgs_sorted[i][j] for j in range(len(nuclei_size_avgs_sorted[i]))]
#     f_stat, p_val = stats.f_oneway(*groups)
#     print(f"Week {i+1}: ANOVA across doses, p = {p_val:.4e}")


# # #2 way anova, does the dose depend on the week?
# import pandas as pd
# import statsmodels.api as sm
# from statsmodels.formula.api import ols

# records = []
# for i, week in enumerate(x_labels_sorted):       # 9 weeks
#     for j, dose in enumerate(range(len(nuclei_size_avgs_sorted[0]))):  # 6 doses
#         for value in nuclei_size_avgs_sorted[i][j]:
#             records.append({"week": week, "dose": f"Dose_{j+1}", "size": value})

# df = pd.DataFrame(records)

# # Two-way ANOVA
# model = ols("size ~ C(week) + C(dose) + C(week):C(dose)", data=df).fit()
# anova_table = sm.stats.anova_lm(model, typ=2)
# print(anova_table)

