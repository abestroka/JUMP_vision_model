import shutil
from pathlib import Path
 
SRC = Path("/grand/projects/FRAME-IDP/astroka/wt_ko/week_nine/results/control/untreated")
DST = Path("/grand/projects/FRAME-IDP/astroka/wt_ko/week_nine/results/confluency_untreated")
 
DST.mkdir(parents=True, exist_ok=True)
 
moved = 0
for src_path in SRC.rglob("*confluency.txt"):
    flat_name = "_".join(src_path.relative_to(SRC).parts)
    dst_path = DST / flat_name
    shutil.move(str(src_path), dst_path)
    print(f"Moved: {src_path.relative_to(SRC)} -> confluency/{flat_name}")
    moved += 1
 
print(f"\nDone. {moved} file(s) moved to {DST}")