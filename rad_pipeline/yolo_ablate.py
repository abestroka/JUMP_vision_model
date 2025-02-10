import os
import glob
import numpy as np
import shutil
import cv2
import yaml
import torch
from collections import defaultdict
from typing import List, Tuple
from tqdm import tqdm
from ultralytics import YOLO

# Define paths
IMAGE_DIR = "/eagle/FoundEpidem/astroka/yolo/rpe_rad_seg_2_vs_8/images/**/*.png"
OUTPUT_FEATURES = "/eagle/FoundEpidem/astroka/yolo/rpe_rad_seg_2_vs_8/features.npz"
TRAIN_DIR = "/eagle/FoundEpidem/astroka/yolo/rpe_rad_seg_2_vs_8/data/dataset/train"
VAL_DIR = "/eagle/FoundEpidem/astroka/yolo/rpe_rad_seg_2_vs_8/data/dataset/val"
CONFIG_PATH = "/eagle/FoundEpidem/astroka/yolo/rpe_rad_seg_2_vs_8/data/datasets/config.yaml"

# Get all image file paths
files = glob.glob(IMAGE_DIR)
print(f"NUM FILES: {len(files)}\n")

def stratified_split_with_groups(filenames: List[str], test_size: float = 0.25, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray]:
    """
    Perform a stratified train/test split while keeping groups intact.
    """
    np.random.seed(random_state)
    compound_groups = defaultdict(dict)

    for idx, filename in enumerate(filenames):
        parts = filename.split('-')
        compound = parts[0]
        group_id = parts[1]
        
        if group_id not in compound_groups[compound]:
            compound_groups[compound][group_id] = []
        compound_groups[compound][group_id].append(idx)

    test_groups_target = {compound: max(1, int(len(groups) * test_size)) for compound, groups in compound_groups.items()}
    
    train_indices, test_indices = [], []
    for compound, groups in compound_groups.items():
        group_ids = list(groups.keys())
        np.random.shuffle(group_ids)

        n_test = test_groups_target[compound]
        for group_id in group_ids[:n_test]:
            test_indices.extend(compound_groups[compound][group_id])
        for group_id in group_ids[n_test:]:
            train_indices.extend(compound_groups[compound][group_id])

    return np.array(train_indices), np.array(test_indices)

# Extract dataset fields
fields = [x.split('/')[-2] + '-' + x.split('/')[-1][:9] for x in files]
train_idx, test_idx = stratified_split_with_groups(fields)

def prepare_classification_data(images, labels, output_dir):
    """
    Organize images into class-labeled folders.
    """
    os.makedirs(output_dir, exist_ok=True)

    for img_path, label in zip(images, labels):
        class_dir = os.path.join(output_dir, str(label))
        os.makedirs(class_dir, exist_ok=True)
        
        img_name = img_path.split('/')[-4] + '_' + os.path.basename(img_path)
        shutil.copy2(img_path, os.path.join(class_dir, img_name))

    return output_dir

labels = [x.split('/')[-2] for x in files]

train_dir = prepare_classification_data(np.array(files)[train_idx], np.array(labels)[train_idx], TRAIN_DIR)
val_dir = prepare_classification_data(np.array(files)[test_idx], np.array(labels)[test_idx], VAL_DIR)

def setup_classification_config(train_dir, val_dir, class_names, config_path):
    """
    Create YOLO classification YAML configuration.
    """
    train_dir, val_dir = os.path.abspath(train_dir), os.path.abspath(val_dir)
    data_yaml = {
        'path': os.path.dirname(train_dir),
        'train': train_dir,
        'val': val_dir,
        'nc': len(class_names),
        'names': class_names
    }
    
    with open(config_path, 'w') as f:
        yaml.dump(data_yaml, f, default_flow_style=False)

# Define class names
class_names = ['week_two', 'week_nine']
setup_classification_config(train_dir, val_dir, class_names, CONFIG_PATH)

# Load pre-trained YOLO model
model = YOLO("yolo11x-cls.pt")

def extract_features(model, image_paths, output_file):
    """
    Extract features from images using YOLO and save them.
    """
    features, img_names = [], []
    
    for img_path in tqdm(image_paths, desc="Extracting Features"):
        img = cv2.imread(img_path)
        img = cv2.resize(img, (640, 640))
        img = torch.tensor(img).permute(2, 0, 1).unsqueeze(0).float()
        
        with torch.no_grad():
            preds = model(img)  # Extract features
            embedding = preds[0].cpu().numpy()  # Convert to NumPy

        features.append(embedding)
        img_names.append(os.path.basename(img_path))

    np.savez(output_file, features=features, img_names=img_names)
    print(f"Saved extracted features to {output_file}")

extract_features(model, files, OUTPUT_FEATURES)

def mask_image(img_path):
    """
    Perform ablation by masking part of an image.
    """
    img = cv2.imread(img_path)
    img = cv2.resize(img, (640, 640))
    img[200:400, 200:400] = 0  # Mask central region
    return img

# Training the model (Optional)
results = model.train(
    data="/eagle/FoundEpidem/astroka/yolo/rpe_rad_seg_2_vs_8/data/dataset/",
    epochs=100, imgsz=640, batch=24, patience=10,
    name='rpe_rad_seg_2_vs_8', classes=['week_two', 'week_eight']
)
