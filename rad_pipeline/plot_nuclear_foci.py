"""
Plot nuclear foci counts (Children_NucFoci_Count) per treatment dose and color group.

Directory structure expected:
  <base_dir>/
    week_one/results/plate8/<color>_<dose>/*Nuclei*.csv
    week_two/results/plate8/<color>_<dose>/*Nuclei*.csv
    ...

Color groups and their display labels:
  red    -> Caspase_and_Gamma H2ax-641
  orange -> Gamma_H2ax-488
  green  -> Caspase_no_H2ax

Two output figures per run:
  1. foci_by_dose_per_color.png
       For each color group, one subplot comparing median foci count
       across doses (x-axis = dose value, one line per week).
  2. foci_dose_trend.png
       One subplot per color group showing median foci count vs dose
       collapsed across all weeks, with a linear trend line to indicate
       whether foci counts rise or fall as dose increases.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats

# WEEKS = ["week_one", "week_two", "week_three", "week_four", "week_five"]
# WEEK_LABELS = [1, 2, 3, 4, 5]
WEEKS = ["week_one"]
WEEK_LABELS = [1]
PLATE = "plate8"
FOCI_COL = "Children_NucFoci_Count"

COLOR_LABELS = {
    "red":    "Caspase_and_Gamma H2ax-641",
    "orange": "Gamma_H2ax-488",
    "green":  "Caspase_no_H2ax",
}

# Visual colors used to draw each group's lines/bars
GROUP_COLORS = {
    "red":    "#d62728",
    "orange": "#ff7f0e",
    "green":  "#2ca02c",
}

WEEK_PALETTE = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
]


def parse_treatment_dir(name: str) -> tuple[str, float] | None:
    """Parse '<color>_<dose>' directory name.

    Returns (color, dose_float) or None if the name does not match.
    """
    m = re.match(r'^(red|orange|green)_([0-9]*\.?[0-9]+)$', name, re.IGNORECASE)
    if m is None:
        return None
    return m.group(1).lower(), float(m.group(2))


def collect_data(base_dir: Path) -> pd.DataFrame:
    """Walk the directory tree and return one row per nucleus.

    Columns: week (int), color (str), dose (float), foci_count (float)
    """
    records = []
    for week_idx, week in enumerate(WEEKS):
        week_num = WEEK_LABELS[week_idx]
        plate_dir = base_dir / week / "results" / PLATE
        if not plate_dir.exists():
            print(f"  [skip] {plate_dir} not found")
            continue
        for treatment_dir in sorted(plate_dir.iterdir()):
            if not treatment_dir.is_dir():
                continue
            parsed = parse_treatment_dir(treatment_dir.name)
            if parsed is None:
                print(f"  [skip] unrecognised directory name: {treatment_dir.name}")
                continue
            color, dose = parsed

            nuclei_csvs = list(treatment_dir.glob("*Nuclei*.csv"))
            if not nuclei_csvs:
                print(f"  [skip] no Nuclei CSVs in {treatment_dir}")
                continue

            for csv_path in nuclei_csvs:
                try:
                    df = pd.read_csv(csv_path, usecols=[FOCI_COL])
                    for val in df[FOCI_COL].dropna():
                        records.append({
                            "week":       week_num,
                            "color":      color,
                            "dose":       dose,
                            "foci_count": float(val),
                        })
                except Exception as e:
                    print(f"  [error] {csv_path}: {e}")

    return pd.DataFrame(records)


def _is_numeric(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False


def plot_foci_by_dose_per_color(df: pd.DataFrame, output_dir: Path) -> None:
    """Figure 1: one subplot per color group.

    X-axis = dose, one line per week, Y-axis = median foci count per nucleus.
    Error band = IQR (Q1-Q3) across nuclei at that dose/week combination.
    """
    colors_present = [c for c in COLOR_LABELS if c in df["color"].unique()]
    n = len(colors_present)
    if n == 0:
        print("  [skip] no recognised color groups found")
        return

    fig, axes = plt.subplots(1, n, figsize=(6 * n, 5), sharey=False)
    if n == 1:
        axes = [axes]

    for ax, color in zip(axes, colors_present):
        cdf = df[df["color"] == color]
        doses = sorted(cdf["dose"].unique())

        for week_idx, week_num in enumerate(sorted(cdf["week"].unique())):
            wdf = cdf[cdf["week"] == week_num]
            medians, q1s, q3s = [], [], []
            for dose in doses:
                vals = wdf[wdf["dose"] == dose]["foci_count"].dropna()
                medians.append(vals.median() if len(vals) else np.nan)
                q1s.append(np.percentile(vals, 25) if len(vals) else np.nan)
                q3s.append(np.percentile(vals, 75) if len(vals) else np.nan)

            line_color = WEEK_PALETTE[week_idx % len(WEEK_PALETTE)]
            ax.plot(doses, medians, marker="o", linewidth=1.8, markersize=6,
                    label=f"Week {week_num}", color=line_color)
            ax.fill_between(doses, q1s, q3s, alpha=0.12, color=line_color)

        ax.set_title(COLOR_LABELS[color], fontsize=11, fontweight="bold",
                     color=GROUP_COLORS[color])
        ax.set_xlabel("Dose", fontsize=11)
        ax.set_ylabel("Median Foci Count per Nucleus", fontsize=10)
        ax.set_xticks(doses)
        ax.set_xticklabels([str(d) for d in doses], rotation=30, ha="right")
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        ax.legend(fontsize=8, title="Week")

    fig.suptitle("Nuclear Foci Count by Dose and Week", fontsize=14, fontweight="bold", y=1.02)
    fig.tight_layout()
    out_path = output_dir / "foci_by_dose_per_color.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out_path}")


def plot_dose_trend(df: pd.DataFrame, output_dir: Path) -> None:
    """Figure 2: dose-response trend collapsed across all weeks.

    One subplot per color group. X-axis = dose, Y-axis = median foci count
    pooled across all weeks at that dose. Linear regression line and
    Pearson r / p-value annotated on each subplot to indicate trend direction.
    """
    colors_present = [c for c in COLOR_LABELS if c in df["color"].unique()]
    n = len(colors_present)
    if n == 0:
        return

    fig, axes = plt.subplots(1, n, figsize=(6 * n, 5), sharey=False)
    if n == 1:
        axes = [axes]

    for ax, color in zip(axes, colors_present):
        cdf = df[df["color"] == color]
        doses = sorted(cdf["dose"].unique())

        medians, q1s, q3s, ns = [], [], [], []
        for dose in doses:
            vals = cdf[cdf["dose"] == dose]["foci_count"].dropna()
            medians.append(vals.median() if len(vals) else np.nan)
            q1s.append(np.percentile(vals, 25) if len(vals) else np.nan)
            q3s.append(np.percentile(vals, 75) if len(vals) else np.nan)
            ns.append(len(vals))

        gc = GROUP_COLORS[color]
        ax.plot(doses, medians, marker="o", linewidth=2, markersize=7,
                color=gc, label="Median foci")
        ax.fill_between(doses, q1s, q3s, alpha=0.15, color=gc, label="IQR")

        # Linear trend line (fit on median values, weighted by n)
        valid = [(d, m, n_) for d, m, n_ in zip(doses, medians, ns)
                 if not np.isnan(m) and n_ > 0]
        if len(valid) >= 2:
            xv = np.array([v[0] for v in valid])
            yv = np.array([v[1] for v in valid])
            wv = np.array([v[2] for v in valid], dtype=float)
            slope, intercept, r, p, _ = stats.linregress(xv, yv)
            x_line = np.linspace(xv.min(), xv.max(), 200)
            ax.plot(x_line, intercept + slope * x_line, "--", color="black",
                    linewidth=1.5, alpha=0.7, label="Linear trend")
            direction = "increasing" if slope > 0 else "decreasing"
            ax.annotate(
                f"r = {r:.3f}, p = {p:.3f}\nTrend: {direction}",
                xy=(0.05, 0.93), xycoords="axes fraction",
                fontsize=9, va="top",
                bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.7),
            )

        ax.set_title(COLOR_LABELS[color], fontsize=11, fontweight="bold", color=gc)
        ax.set_xlabel("Dose", fontsize=11)
        ax.set_ylabel("Median Foci Count per Nucleus\n(all weeks pooled)", fontsize=10)
        ax.set_xticks(doses)
        ax.set_xticklabels([str(d) for d in doses], rotation=30, ha="right")
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        ax.legend(fontsize=8)

    fig.suptitle("Nuclear Foci Count Dose-Response Trend", fontsize=14,
                 fontweight="bold", y=1.02)
    fig.tight_layout()
    out_path = output_dir / "foci_dose_trend.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out_path}")


def print_summary(df: pd.DataFrame) -> None:
    print("\n--- Summary: median foci count by color and dose (all weeks) ---")
    summary = (
        df.groupby(["color", "dose"])["foci_count"]
        .agg(n="count", median="median",
             q1=lambda x: np.percentile(x, 25),
             q3=lambda x: np.percentile(x, 75))
        .reset_index()
    )
    summary["label"] = summary["color"].map(COLOR_LABELS)
    summary = summary.sort_values(["color", "dose"])
    for _, row in summary.iterrows():
        print(f"  {row['label']} | dose={row['dose']:.4g} | "
              f"n={int(row['n'])} | median={row['median']:.2f} "
              f"[Q1={row['q1']:.2f}, Q3={row['q3']:.2f}]")


def main():
    parser = argparse.ArgumentParser(
        description="Plot nuclear foci counts by dose and color group."
    )
    parser.add_argument(
        "-b", "--base_dir",
        type=Path,
        default=Path("/FRAME-IDP/astroka/rpe_h2a"),
        help="Base experiment directory containing week_one through week_five",
    )
    parser.add_argument(
        "-o", "--output_dir",
        type=Path,
        default=Path("."),
        help="Directory to write output PNGs (default: current directory)",
    )
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    print("Collecting nuclear foci data...")
    df = collect_data(args.base_dir)

    if df.empty:
        print("No data collected — check your base directory and file structure.")
        return

    print(f"Collected {len(df):,} nucleus measurements across "
          f"{df['color'].nunique()} color groups, "
          f"{df['dose'].nunique()} doses, "
          f"{df['week'].nunique()} weeks.")

    print_summary(df)

    print("\nGenerating plots...")
    plot_foci_by_dose_per_color(df, args.output_dir)
    plot_dose_trend(df, args.output_dir)
    print("\nDone.")


if __name__ == "__main__":
    main()
