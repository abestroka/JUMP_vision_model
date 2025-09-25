import os
import numpy as np
import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.formula.api import ols

# -----------------------------
# Config
# -----------------------------
repo_path = "/eagle/projects/FoundEpidem/astroka/rpe/"
doses = ["0.001", "0.01", "0.1", "1.0", "2.0", "untreated"]

# -----------------------------
# Helpers
# -----------------------------
def week_number(label):
    """Extract the week number from folder name like 'week_one'."""
    words_to_nums = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9
    }
    word = label.split("_")[1].lower()
    return words_to_nums.get(word, None)

# -----------------------------
# Collect all data into tidy format
# -----------------------------
records = []

week_folders = [f for f in os.listdir(repo_path) if f.startswith("week_")]

for week in week_folders:
    week_num = week_number(week)
    if week_num is None:
        continue

    # RAD treated
    week_path = os.path.join(repo_path, week, "sheets", "rpe_rad")
    if os.path.isdir(week_path):
        for dose in doses[:-1]:  # skip "untreated" here
            dose_path = os.path.join(week_path, dose)
            if not os.path.isdir(dose_path):
                continue
            for file in os.listdir(dose_path):
                if file.endswith("nuclei.csv"):
                    df = pd.read_csv(os.path.join(dose_path, file))
                    for col in df.select_dtypes(include=[np.number]).columns:
                        for val in df[col].dropna():
                            records.append({
                                "week": week_num,
                                "dose": dose,
                                "feature": col,
                                "value": val
                            })

    # Untreated control
    control_path = os.path.join(repo_path, week, "sheets", "rpe_control", "untreated")
    if os.path.isdir(control_path):
        for file in os.listdir(control_path):
            if file.endswith("nuclei.csv"):
                df = pd.read_csv(os.path.join(control_path, file))
                for col in df.select_dtypes(include=[np.number]).columns:
                    for val in df[col].dropna():
                        records.append({
                            "week": week_num,
                            "dose": "untreated",
                            "feature": col,
                            "value": val
                        })

# Make tidy DataFrame
df_all = pd.DataFrame(records)
print(f"Collected {len(df_all)} measurements across {df_all['feature'].nunique()} features.")

# -----------------------------
# One-way ANOVA: effect of week (pooled doses)
# -----------------------------
features = df_all["feature"].unique()
week_results = {}

for feat in features:
    subset = df_all[df_all["feature"] == feat]
    groups = [g["value"].values for _, g in subset.groupby("week")]
    if len(groups) > 1:
        f, p = stats.f_oneway(*groups)
        week_results[feat] = p

# -----------------------------
# One-way ANOVA: effect of dose (pooled weeks)
# -----------------------------
dose_results = {}
for feat in features:
    subset = df_all[df_all["feature"] == feat]
    groups = [g["value"].values for _, g in subset.groupby("dose")]
    if len(groups) > 1:
        f, p = stats.f_oneway(*groups)
        dose_results[feat] = p

# -----------------------------
# Two-way ANOVA: week + dose
# -----------------------------
two_way_results = {}
for feat in features:
    subset = df_all[df_all["feature"] == feat]
    if subset["week"].nunique() > 1 and subset["dose"].nunique() > 1:
        model = ols("value ~ C(week) + C(dose) + C(week):C(dose)", data=subset).fit()
        anova_table = sm.stats.anova_lm(model, typ=2)
        two_way_results[feat] = anova_table

# -----------------------------
# Print ranked results
# -----------------------------
week_ranked = sorted(week_results.items(), key=lambda x: x[1])
dose_ranked = sorted(dose_results.items(), key=lambda x: x[1])

print("\nMost significant features across weeks (one-way ANOVA):")
for feat, p in week_ranked[:10]:
    print(f"{feat:25s}  p={p:.3e}")

print("\nMost significant features across doses (one-way ANOVA):")
for feat, p in dose_ranked[:10]:
    print(f"{feat:25s}  p={p:.3e}")

print("\nExample two-way ANOVA results for top week feature:")
if week_ranked:
    feat = week_ranked[0][0]
    print(f"\nFeature: {feat}")
    print(two_way_results[feat])

print("\nExample two-way ANOVA results for top dose feature:")
if dose_ranked:
    feat = dose_ranked[0][0]
    print(f"\nFeature: {feat}")
    print(two_way_results[feat])
