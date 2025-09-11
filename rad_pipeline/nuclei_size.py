import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

repo_path = "/eagle/projects/FoundEpidem/astroka/ten_week/"

nuclei_size_avgs = []
doses = []
type = "huvec_rad"

week_folders = [f for f in os.listdir(repo_path) if f.startswith("week_")]

for week in week_folders:
    week_path = os.path.join(repo_path, week, "results", type)
