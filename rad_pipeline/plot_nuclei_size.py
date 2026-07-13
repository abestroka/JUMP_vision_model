"""
Plot median nuclei area (AreaShape_Area) per treatment across weeks,
one figure per plate (Plate3, Plate8, Control).

Directory structure expected:
  <base_dir>/
    week_one/results/<plate>/<treatment>/*_nuclei.csv
    week_two/results/<plate>/<treatment>/*_nuclei.csv
    ...
    week_five/results/<plate>/<treatment>/*_nuclei.csv
"""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd

WEEKS = ["week_one", "week_two", "week_three", "week_four", "week_five"]
WEEK_LABELS = [1, 2, 3, 4, 5]
PLATES = ["Plate3", "Plate8", "Control"]

# Plates where we overlay the median cell count line
COUNT_PLATES = {"Plate3", "Plate8"}


def collect_data(base_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Walk the directory tree and collect nuclei area and cell count data.

    Returns
    -------
    nuclei_df : DataFrame
        One row per nucleus with columns: week, plate, treatment, area
    counts_df : DataFrame
        One row per image with columns: week, plate, count_cells
    """
    nuclei_records = []
    count_records = []

    for week_idx, week in enumerate(WEEKS):
        week_num = WEEK_LABELS[week_idx]
        for plate in PLATES:
            plate_dir = base_dir / week / "results" / plate
            if not plate_dir.exists():
                print(f"  [skip] {plate_dir} not found")
                continue
            for treatment_dir in sorted(plate_dir.iterdir()):
                if not treatment_dir.is_dir():
                    continue
                treatment = treatment_dir.name

                # --- nuclei area ---
                nuclei_csvs = list(treatment_dir.glob("*_nuclei.csv"))
                if not nuclei_csvs:
                    print(f"  [skip] no nuclei CSVs in {treatment_dir}")
                else:
                    for csv_path in nuclei_csvs:
                        try:
                            df = pd.read_csv(csv_path, usecols=["AreaShape_Area"])
                            for area in df["AreaShape_Area"].dropna():
                                nuclei_records.append({
                                    "week": week_num,
                                    "plate": plate,
                                    "treatment": treatment,
                                    "area": area,
                                })
                        except Exception as e:
                            print(f"  [error] {csv_path}: {e}")

                # --- cell counts (image CSVs) ---
                image_csvs = list(treatment_dir.glob("*_image.csv"))
                for csv_path in image_csvs:
                    try:
                        df = pd.read_csv(csv_path, usecols=["Count_Cells"])
                        for count in df["Count_Cells"].dropna():
                            count_records.append({
                                "week": week_num,
                                "plate": plate,
                                "count_cells": count,
                            })
                    except Exception as e:
                        print(f"  [error] {csv_path}: {e}")

    return pd.DataFrame(nuclei_records), pd.DataFrame(count_records)


def make_color_palette(n: int) -> list:
    """Return n visually distinct colors.

    For n <= 10 uses tab10; for larger n samples from a high-contrast
    composite of tab10, tab20b, and tab20c to keep colors distinct.
    """
    if n <= 10:
        cmap = plt.get_cmap("tab10")
        return [cmap(i) for i in range(n)]

    # Build a diverse pool from three qualitative maps, deduplicated
    pool = []
    for cmap_name in ("tab20", "tab20b", "tab20c"):
        cmap = plt.get_cmap(cmap_name)
        pool.extend([cmap(i) for i in range(cmap.N)])

    # Space the picks evenly across the pool for maximum spread
    step = len(pool) / n
    return [pool[int(i * step) % len(pool)] for i in range(n)]


def plot_plate(
    nuclei_df: pd.DataFrame,
    counts_df: pd.DataFrame,
    plate: str,
    output_dir: Path,
) -> None:
    """Create and save a median nuclei size plot for one plate."""
    plate_data = nuclei_df[nuclei_df["plate"] == plate]
    if plate_data.empty:
        print(f"  [skip] no data for {plate}")
        return

    # Compute median per treatment per week
    summary = (
        plate_data.groupby(["treatment", "week"])["area"]
        .agg(
            median="median",
            q1=lambda x: np.percentile(x, 25),
            q3=lambda x: np.percentile(x, 75),
            n="count",
        )
        .reset_index()
    )

    treatments = sorted(
        summary["treatment"].unique(),
        key=lambda t: (0, float(t)) if _is_numeric(t) else (1, t),
    )

    colors = make_color_palette(len(treatments))

    # Dual y-axis only for Plate3 and Plate8
    use_count_axis = plate in COUNT_PLATES
    fig, ax1 = plt.subplots(figsize=(9, 5))

    for i, treatment in enumerate(treatments):
        tdata = summary[summary["treatment"] == treatment].sort_values("week")
        ax1.plot(
            tdata["week"].values,
            tdata["median"].values,
            label=treatment,
            marker="o",
            linewidth=1.8,
            markersize=6,
            color=colors[i],
        )

    ax1.set_xticks(WEEK_LABELS)
    ax1.set_xticklabels([f"Week {w}" for w in WEEK_LABELS])
    ax1.set_xlabel("Week", fontsize=12)
    ax1.set_ylabel("Median Nuclei Area (pixels²)", fontsize=12)
    ax1.grid(axis="y", linestyle="--", alpha=0.4)

    if use_count_axis:
        plate_counts = counts_df[counts_df["plate"] == plate]
        if not plate_counts.empty:
            count_summary = (
                plate_counts.groupby("week")["count_cells"]
                .median()
                .reset_index()
                .sort_values("week")
            )
            ax2 = ax1.twinx()
            ax2.plot(
                count_summary["week"].values,
                count_summary["count_cells"].values,
                label="Median Cell Count",
                color="black",
                linewidth=2.5,
                linestyle="--",
                marker="s",
                markersize=7,
                zorder=10,
            )
            ax2.set_ylabel("Median Cell Count", fontsize=12)
            # Add cell count line to legend
            handles2, labels2 = ax2.get_legend_handles_labels()
            handles1, labels1 = ax1.get_legend_handles_labels()
            ax1.legend(
                handles1 + handles2,
                labels1 + labels2,
                title="Treatment",
                bbox_to_anchor=(1.12, 1),
                loc="upper left",
                fontsize=9,
            )
        else:
            ax1.legend(title="Treatment", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=9)
    else:
        ax1.legend(title="Treatment", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=9)

    ax1.set_title(f"Median Nuclei Size Over Time — {plate}", fontsize=13, fontweight="bold")
    fig.tight_layout()

    out_path = output_dir / f"nuclei_size_{plate}.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out_path}")


def _is_numeric(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False


def main():
    parser = argparse.ArgumentParser(description="Plot median nuclei size per treatment/week/plate.")
    parser.add_argument(
        "-b", "--base_dir",
        type=Path,
        default=Path("/FRAME-IDP/astroka/exp_05_26"),
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

    print("Collecting nuclei data...")
    nuclei_df, counts_df = collect_data(args.base_dir)

    if nuclei_df.empty:
        print("No data collected — check your base directory and file structure.")
        return

    print(f"Collected {len(nuclei_df):,} nuclei measurements across "
          f"{nuclei_df['plate'].nunique()} plates, "
          f"{nuclei_df['treatment'].nunique()} treatments, "
          f"{nuclei_df['week'].nunique()} weeks.")
    print(f"Collected {len(counts_df):,} image-level cell count records.")

    print("\nGenerating plots...")
    for plate in PLATES:
        plot_plate(nuclei_df, counts_df, plate, args.output_dir)

    print("\nDone.")


if __name__ == "__main__":
    main()