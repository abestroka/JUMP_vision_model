from __future__ import annotations

import shutil
from pathlib import Path
import pandas as pd
from tqdm import tqdm

# Paths and parameters
treatment_path = Path("/home/astroka/workspace/JUMP_vision_model/rad_pipeline/week_three_fib_layout.xlsx")
plate = "fib_rad"
image_path = Path("/eagle/FoundEpidem/astroka/fib_and_htert/week_three/20241009_NewWeek3/20241009_ANL_CellPainting_W3P3_1__2024-10-09T22_29_20-Measurement1/Images")
destination_root = Path("/eagle/FoundEpidem/astroka/fib_and_htert/week_three/ch2_tiffs/")

# Read treatment layout
treatments = pd.read_excel(treatment_path, sheet_name=plate)

# Iterate through each treatment/location row
for _, row in tqdm(treatments.iterrows(), total=len(treatments), desc="Processing wells"):
    location = str(row["Location"]).strip()   # e.g., r00c00
    treatment = str(row["Treatment"]).strip() # e.g., "DMSO"

    # Find all matching image files that contain 'ch2'
    well_images = [f for f in image_path.glob(f"{location}*ch2*") if f.is_file()]

    if not well_images:
        print(f"⚠️ No ch2 images found for {location}")
        continue

    # Create destination folder named after treatment
    dest_path = destination_root / treatment
    dest_path.mkdir(parents=True, exist_ok=True)

    # Move all matching images
    for img_file in well_images:
        shutil.move(str(img_file), dest_path / img_file.name)

print("✅ All matching ch2 images moved successfully.")
