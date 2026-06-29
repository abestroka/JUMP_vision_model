"""
Plot median nuclei area (AreaShape_Area) per treatment across weeks,
one figure per plate (Plate3, Plate8, Control).

Directory structure expected:
  <base_dir>/
    week_one/results/<plate>/<treatment>/*_nuclei.csv
    week_two/results/<plate>/<treatment>/*_nuclei.csv
    week_three/results/<plate>/<treatment>/*_nuclei.csv
"""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

WEEKS = ["week_one", "week_two", "week_three"]
WEEK_LABELS = [1, 2, 3]
PLATES = ["Plate3", "Plate8", "Control"]


def collect_data(base_dir: Path) -> pd.DataFrame:
    """Walk the directory tree and collect all nuclei CSV data."""
    records = []
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
                nuclei_csvs = list(treatment_dir.glob("*_nuclei.csv"))
                if not nuclei_csvs:
                    print(f"  [skip] no nuclei CSVs in {treatment_dir}")
                    continue
                for csv_path in nuclei_csvs:
                    try:
                        df = pd.read_csv(csv_path, usecols=["AreaShape_Area"])
                        for area in df["AreaShape_Area"].dropna():
                            records.append({
                                "week": week_num,
                                "plate": plate,
                                "treatment": treatment,
                                "area": area,
                            })
                    except Exception as e:
                        print(f"  [error] {csv_path}: {e}")
    return pd.DataFrame(records)


def plot_plate(data: pd.DataFrame, plate: str, output_dir: Path) -> None:
    """Create and save a median nuclei size plot for one plate."""
    plate_data = data[data["plate"] == plate]
    if plate_data.empty:
        print(f"  [skip] no data for {plate}")
        return

    # Compute median and IQR (Q1/Q3) per treatment per week
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

    # treatments = sorted(summary["treatment"].unique(), key=lambda t: float(t) if _is_numeric(t) else t)
    treatments = sorted(
        summary["treatment"].unique(),
        key=lambda t: (0, float(t)) if _is_numeric(t) else (1, t)
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    cmap = plt.get_cmap("tab10")

    for i, treatment in enumerate(treatments):
        tdata = summary[summary["treatment"] == treatment].sort_values("week")
        weeks = tdata["week"].values
        medians = tdata["median"].values
        lower_err = medians - tdata["q1"].values
        upper_err = tdata["q3"].values - medians

        color = cmap(i % 10)
        ax.errorbar(
            weeks,
            medians,
            yerr=[lower_err, upper_err],
            label=treatment,
            marker="o",
            capsize=4,
            linewidth=1.8,
            markersize=6,
            color=color,
        )

    ax.set_xticks(WEEK_LABELS)
    ax.set_xticklabels([f"Week {w}" for w in WEEK_LABELS])
    ax.set_xlabel("Week", fontsize=12)
    ax.set_ylabel("Median Nuclei Area (pixels²)", fontsize=12)
    ax.set_title(f"Median Nuclei Size Over Time — {plate}", fontsize=13, fontweight="bold")
    ax.legend(title="Treatment", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=9)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
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
        help="Base experiment directory containing week_one/week_two/week_three",
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
    data = collect_data(args.base_dir)

    if data.empty:
        print("No data collected — check your base directory and file structure.")
        return

    print(f"Collected {len(data):,} nuclei measurements across "
          f"{data['plate'].nunique()} plates, "
          f"{data['treatment'].nunique()} treatments, "
          f"{data['week'].nunique()} weeks.")

    print("\nGenerating plots...")
    for plate in PLATES:
        plot_plate(data, plate, args.output_dir)

    print("\nDone.")


if __name__ == "__main__":
    main()
