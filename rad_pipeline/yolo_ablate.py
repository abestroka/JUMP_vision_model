import os
import glob
import shutil
import numpy as np
import yaml
from collections import defaultdict
from typing import List, Tuple
from ultralytics import YOLO
import torch

# Load Image Paths
files = glob.glob('/eagle/FoundEpidem/astroka/yolo/rpe_rad_seg_2_vs_8/images/**/*.png')

print("NUM FILES:", len(files))

# Stratified Train/Test Split
def stratified_split_with_groups(filenames: List[str], test_size: float = 0.25, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray]:
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

fields = [x.split('/')[-2] + '-' + x.split('/')[-1][:9] for x in files]
train_idx, test_idx = stratified_split_with_groups(fields)

# Organize images into class folders
def prepare_classification_data(images, labels, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for img_path, label in zip(images, labels):
        class_dir = os.path.join(output_dir, str(label))
        os.makedirs(class_dir, exist_ok=True)
        wk = img_path.split('/')[-4]
        img_name = wk + '_' + os.path.basename(img_path)
        shutil.copy2(img_path, os.path.join(class_dir, img_name))
    return output_dir

labels = [x.split('/')[-2] for x in files]
train_dir = prepare_classification_data(np.array(files)[train_idx], np.array(labels)[train_idx], '/eagle/FoundEpidem/astroka/yolo/rpe_rad_seg_2_vs_8/data/dataset/train')
val_dir = prepare_classification_data(np.array(files)[test_idx], np.array(labels)[test_idx], '/eagle/FoundEpidem/astroka/yolo/rpe_rad_seg_2_vs_8/data/dataset/val')

# Setup YAML config
def setup_classification_config(train_dir, val_dir, class_names, config_path):
    data_yaml = {
        'path': os.path.dirname(train_dir),
        'train': os.path.abspath(train_dir),
        'val': os.path.abspath(val_dir),
        'nc': len(class_names),
        'names': class_names
    }
    with open(config_path, 'w') as f:
        yaml.dump(data_yaml, f, default_flow_style=False)

class_names = ['week_two', 'week_eight']
setup_classification_config(train_dir, val_dir, class_names, '/eagle/FoundEpidem/astroka/yolo/rpe_rad_seg_2_vs_8/data/datasets/config.yaml')

# Load YOLO Model (Feature Extraction)
model = YOLO("yolo11x-cls.pt")

# Feature Extraction from YOLO
def extract_features(model, image_paths):
    """
    Extracts deep features from YOLO backbone (before classification head)
    """
    features = []
    for img_path in image_paths:
        results = model(img_path, feature=True)  # Extract features
        feature_vector = results[0].features.cpu().numpy()  # Convert to numpy
        features.append(feature_vector)
    return np.array(features)

# Extract features for Train and Validation
train_features = extract_features(model, np.array(files)[train_idx])
val_features = extract_features(model, np.array(files)[test_idx])

# Save Features
np.save('/eagle/FoundEpidem/astroka/yolo/rpe_rad_seg_2_vs_8/features/train_features.npy', train_features)
np.save('/eagle/FoundEpidem/astroka/yolo/rpe_rad_seg_2_vs_8/features/val_features.npy', val_features)

# Ablation Study: Remove Specific Features
def ablate_features(features, method='random_zero'):
    """
    Perform ablation on extracted features.
    - method='random_zero': Randomly zero out some feature elements.
    - method='remove_first_half': Remove the first half of feature dimensions.
    - method='remove_last_half': Remove the last half of feature dimensions.
    """
    ablated_features = features.copy()
    if method == 'random_zero':
        mask = np.random.rand(*features.shape) > 0.5  # 50% chance to zero out features
        ablated_features *= mask
    elif method == 'remove_first_half':
        ablated_features[:, :features.shape[1] // 2] = 0
    elif method == 'remove_last_half':
        ablated_features[:, features.shape[1] // 2:] = 0
    return ablated_features

# Apply ablation
train_features_ablation = ablate_features(train_features, method='random_zero')
val_features_ablation = ablate_features(val_features, method='random_zero')

# Save Ablated Features
np.save('/eagle/FoundEpidem/astroka/yolo/rpe_rad_seg_2_vs_8/features/train_features_ablation.npy', train_features_ablation)
np.save('/eagle/FoundEpidem/astroka/yolo/rpe_rad_seg_2_vs_8/features/val_features_ablation.npy', val_features_ablation)

# Train with Ablated Features
results = model.train(data="/eagle/FoundEpidem/astroka/yolo/rpe_rad_seg_2_vs_8/data/dataset/", epochs=100, imgsz=640, batch=24, patience=10, name='rpe_rad_seg_2_vs_8_ablation', classes=['week_two', 'week_eight'])
