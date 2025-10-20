# import os
# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd
# from statistics import mean

# repo_path = "/eagle/projects/FoundEpidem/astroka/fib_and_htert/"

# nuclei_size_avgs = []
# doses = ["0.001", "0.01", "0.1", "1.0", "2.0"]
# weeks = []
# type = "fib_rad"
# results = {dose: [] for dose in doses}

# week_folders = [f for f in os.listdir(repo_path) if f.startswith("week_")]

# for week in week_folders:
#     week_path = os.path.join(repo_path, week, "sheets", "fib_rad")
#     if not os.path.isdir(week_path):
#         continue

#     week_vals = []

#     for dose in doses:
#         dose_path = os.path.join(week_path, dose)
#         if not os.path.isdir(dose_path):
#             results[dose].append(np.nan)
#             continue
        
#         values = []
#         for file in os.listdir(dose_path):
#             if file.endswith("nuclei.csv"):
#                 df = pd.read_csv(os.path.join(dose_path, file))
#                 col_data = df["AreaShape_Area"].tolist()
#                 # print("RAD", col_data)
#                 if col_data != []:

#                     values.append(mean(col_data))
        
#         week_vals.append(values)
    
#     weeks.append(week)

# ################

#     dose_path = os.path.join(repo_path, week, "sheets", "fib_control", "untreated")
        
#     values = []
#     for file in os.listdir(dose_path):
#         if file.endswith("nuclei.csv"):
#             df = pd.read_csv(os.path.join(dose_path, file))
#             col_data = df["AreaShape_Area"].tolist()
#             # print("UNTREATED", col_data)
#             if col_data != []:
#                 values.append(mean(col_data))
#     week_vals.append(values)

#     nuclei_size_avgs.append(week_vals)




# doses.append("untreated")


# ##########

# import re

# def week_number(label):
#     """Extract the week number from a string like 'week_one' -> 1"""
#     # If they're written as words like "one", "two" etc
#     words_to_nums = {
#         "one": 1, "two": 2, "three": 3, "four": 4
#     }
#     word = label.split("_")[1].lower()
#     return words_to_nums[word]

# # Pair labels with their data
# x_labels = weeks
# paired = list(zip(x_labels, nuclei_size_avgs))

# # Sort by extracted week number
# paired_sorted = sorted(paired, key=lambda x: week_number(x[0]))

# # Unpack back into labels and data
# x_labels_sorted, nuclei_size_avgs_sorted = zip(*paired_sorted)

# # Convert nuclei_size_avgs_sorted back into a list
# nuclei_size_avgs_sorted = list(nuclei_size_avgs_sorted)

# nuclei_size_avgs = nuclei_size_avgs_sorted
# #############

# # colors = plt.cm.tab10.colors[:data.shape[1]]  # 6 distinct colors

# colors = plt.cm.tab10.colors[:len(nuclei_size_avgs[0])]

# fig, axes = plt.subplots(1, len(nuclei_size_avgs[0]), figsize=(20, 6), sharey=True)
# # x_labels = [f"Week {i+1}" for i in range(len(nuclei_size_avgs))]
# print(weeks)
# x_labels = weeks
# # for j in range(len(nuclei_size_avgs[0])):  # 6 groups
#     # Collect data for this group: list of 9 arrays, each length 180
#     # group_data = [nuclei_size_avgs[i][j] for i in range(len(nuclei_size_avgs))]

# for j in range(max(len(row) for row in nuclei_size_avgs)):  # up to max groups
#     group_data = [nuclei_size_avgs[i][j] for i in range(len(nuclei_size_avgs)) if j < len(nuclei_size_avgs[i])]
#     # now plot group_data

    
#     bp = axes[j].boxplot(group_data, patch_artist=True, widths=0.6)
    
#     # Color the boxes
#     for patch in bp['boxes']:
#         patch.set_facecolor(colors[j])
#         patch.set_alpha(0.6)
    
#     axes[j].set_xticks(range(1, len(nuclei_size_avgs) + 1))
#     axes[j].set_xticklabels(x_labels_sorted, rotation=45, ha="right")
#     axes[j].set_title(doses[j])
#     axes[j].set_yscale("log")


# axes[0].set_ylabel("Nuclei Size")
# plt.tight_layout()
# # plt.show()

# repo_path = "/eagle/projects/FoundEpidem/astroka/fib_and_htert/"

# png_path = os.path.join(repo_path, "average_nuclei_size.png")
# plt.savefig(png_path, dpi=300)
# plt.close()

# def anova_eta_squared(groups):
#     # groups = list of lists
#     all_data = np.concatenate(groups)
#     grand_mean = np.mean(all_data)
    
#     # between-group SS
#     ss_between = sum(len(g) * (np.mean(g) - grand_mean) ** 2 for g in groups)
#     # total SS
#     ss_total = sum(((x - grand_mean) ** 2).sum() for g in groups for x in g)
    
#     return ss_between / ss_total

# # for dose x, does nucleus size change across weeks?

# # import scipy.stats as stats

# # p_values = []
# # for j in range(len(nuclei_size_avgs_sorted[0])):  # loop doses
# #     # Gather data: 9 groups (weeks), each with replicates
# #     groups = []
# #     for i in range(len(nuclei_size_avgs_sorted)):
# #         if j < len(nuclei_size_avgs_sorted[i]):  # only if this dose exists in that week
# #             if len(nuclei_size_avgs_sorted[i][j]) > 0:  # skip empty lists
# #                 groups.append(nuclei_size_avgs_sorted[i][j])
# #     # groups = [nuclei_size_avgs_sorted[i][j] for i in range(len(nuclei_size_avgs_sorted))]
# #     if len(groups) > 1:
# #         f_stat, p_val = stats.f_oneway(*groups)
# #         p_values.append(p_val)
# #         eta2 = anova_eta_squared(groups)
# #         print(f"F={f_stat:.2f}, p={p_val:.2e}, η²={eta2:.3f}")

# #         print(f"Dose {doses[j]}: ANOVA across weeks, p = {p_val:.4e}")
# #     else:
# #         print(f"Dose {doses[j]}: not enough data for ANOVA")



# # p_values = []
# # # at week n, does nuclues size differ between doses?
# # for i in range(len(nuclei_size_avgs_sorted)):  # loop weeks
# #     groups = []
# #     for j in range(len(nuclei_size_avgs_sorted[i])):  # loop doses within that week
# #         if len(nuclei_size_avgs_sorted[i][j]) > 0:
# #             groups.append(nuclei_size_avgs_sorted[i][j])
# #     if len(groups) > 1:
# #         f_stat, p_val = stats.f_oneway(*groups)
# #         p_values.append(p_val)
# #         eta2 = anova_eta_squared(groups)
# #         print(f"F={f_stat:.2f}, p={p_val:.2e}, η²={eta2:.3f}")
# #         print(f"Week {i+1}: ANOVA across doses, p = {p_val:.4e}")
# #     else:
# #         print(f"Week {i+1}: not enough data for ANOVA")


import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

repo_path = "/eagle/projects/FoundEpidem/astroka/fib_and_htert/"

doses = ["0.001", "0.01", "0.1", "1.0", "2.0", "untreated"]
type = "fib_rad"

# Dictionary to store ALL cell areas across all weeks for each dose
dose_cell_areas = {dose: [] for dose in doses}

# Iterate through all week folders
week_folders = [f for f in os.listdir(repo_path) if f.startswith("week_")]

for week in week_folders:
    # --- RADIATED samples ---
    rad_path = os.path.join(repo_path, week, "sheets", "fib_rad")
    if os.path.isdir(rad_path):
        for dose in doses[:-1]:  # all except untreated
            dose_path = os.path.join(rad_path, dose)
            if not os.path.isdir(dose_path):
                continue
            for file in os.listdir(dose_path):
                if file.endswith("nuclei.csv"):
                    df = pd.read_csv(os.path.join(dose_path, file))
                    if "AreaShape_Area" in df.columns:
                        col_data = df["AreaShape_Area"].dropna().tolist()
                        dose_cell_areas[dose].extend(col_data)
    
    # --- UNTREATED control ---
    control_path = os.path.join(repo_path, week, "sheets", "fib_control", "untreated")
    if os.path.isdir(control_path):
        for file in os.listdir(control_path):
            if file.endswith("nuclei.csv"):
                df = pd.read_csv(os.path.join(control_path, file))
                if "AreaShape_Area" in df.columns:
                    col_data = df["AreaShape_Area"].dropna().tolist()
                    dose_cell_areas["untreated"].extend(col_data)


# ----------- PLOT HISTOGRAMS -----------
fig, axes = plt.subplots(1, len(doses), figsize=(22, 5), sharey=True)

bins = np.arange(0, 5000 + 250, 250)  # Adjust range as needed

for ax, dose in zip(axes, doses):
    data = dose_cell_areas[dose]
    ax.hist(data, bins=bins, color="steelblue", edgecolor="black", alpha=0.7)
    ax.set_title(dose)
    ax.set_xlabel("Cell area (µm²)")
    ax.set_xlim([0, bins[-1]])
    ax.grid(alpha=0.3)

axes[0].set_ylabel("Number of cells")
plt.tight_layout()

png_path = os.path.join(repo_path, "nuclei_area_histograms.png")
plt.savefig(png_path, dpi=300)
plt.close()

print(f"Saved histograms to {png_path}")
