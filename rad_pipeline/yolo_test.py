import glob
import pandas as pd
from collections import defaultdict
import numpy as np
from typing import List, Dict, Set, Tuple

from ultralytics import YOLO
import yaml
from pathlib import Path
import pandas as pd
import shutil
import os

import random

# Path to the images directory
base_path = '/eagle/FoundEpidem/astroka/yolo/huvec_control_seg_1/images/'

# Number of files to keep in each subdirectory
num_files_to_keep = 500

# Find all subdirectories under the images directory
subdirs = [d for d in glob.glob(os.path.join(base_path, '*')) if os.path.isdir(d)]

for subdir in subdirs:
    # Find all PNG files in the current subdirectory
    files = glob.glob(os.path.join(subdir, '*.png'))
    
    # If the number of files exceeds the limit, delete extras
    if len(files) > num_files_to_keep:
        files_to_delete = random.sample(files, len(files) - num_files_to_keep)
        for file in files_to_delete:
            os.remove(file)
        print(f"Deleted {len(files_to_delete)} files from {subdir}")
    else:
        print(f"{subdir} has {len(files)} files, no files deleted.")

##############
##########


# files = glob.glob('/eagle/FoundEpidem/astroka/yolo/rpe_rad_seg_1/images/**/*p05.png')
files = glob.glob('/eagle/FoundEpidem/astroka/yolo/huvec_control_seg_1/images/**/*.png')
# print("NUM FILES")
# print(len(files))
# print(" ")


def stratified_split_with_groups(
    filenames: List[str], 
    test_size: float = 0.25,
    random_state: int = 42
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Create a stratified train/test split while keeping samples with the same ID in the same split.
    Returns indexes that can be used to split both filenames and labels.
    
    Args:
        filenames: List of filenames in format 'Compound_X_rXXcXXfXX'
        test_size: Proportion of data to use for test set
        random_state: Random seed for reproducibility
        
    Returns:
        Tuple of (train_indices, test_indices) as numpy arrays
    """
    np.random.seed(random_state)
    
    # Extract compound numbers and IDs
    compound_groups = defaultdict(dict)

    
    # Create mapping of groups to their indices
    for idx, filename in enumerate(filenames):
        parts = filename.split('-')
        compound = parts[0]  # e.g., "Compound_10"
        group_id = parts[1]  # e.g., "r02c02f07"
        # print("COMPOUND", compound)
        # print("GROUP ID", group_id)
        # print(" ")
        
        if group_id not in compound_groups[compound]:
            compound_groups[compound][group_id] = []
        compound_groups[compound][group_id].append(idx)
    
    # print('COMPOUND GROUPS')
    # print(compound_groups)
    # print(" ")
    # Calculate target number of groups per compound in test set
    test_groups_target = {
        compound: max(1, int(len(groups) * test_size))
        for compound, groups in compound_groups.items()
    }
    
    # Randomly select groups for test and train sets
    train_indices = []
    test_indices = []
    
    for compound, groups in compound_groups.items():
        group_ids = list(groups.keys())
        np.random.shuffle(group_ids)
        
        n_test = test_groups_target[compound]
        
        # Add all indices from test groups
        for group_id in group_ids[:n_test]:
            test_indices.extend(compound_groups[compound][group_id])
            
        # Add all indices from train groups
        for group_id in group_ids[n_test:]:
            train_indices.extend(compound_groups[compound][group_id])
    
    return np.array(train_indices), np.array(test_indices)

fields = [x.split('/')[-2] + '-' + x.split('/')[-1][:9] for x in files]

# print("FIELDS[0]")
# print(fields[0])


train_idx, test_idx = stratified_split_with_groups(fields)


def prepare_classification_data(images, labels, output_dir):
    """
    Organize images into class folders based on external label list
    
    Args:
        image_list (str): Path to file containing image paths
        label_list (str): Path to file containing corresponding labels
        output_dir (str): Directory to store organized dataset
    Returns:
        str: Path to organized dataset directory
    """
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
        
    # Create class directories and copy images
    for img_path, label in zip(images, labels):
        # Create class directory if it doesn't exist
        class_dir = os.path.join(output_dir, str(label))
        os.makedirs(class_dir, exist_ok=True)
        
        wk = img_path.split('/')[-4]
        # Copy image to class directory
        img_name = wk + '_' + os.path.basename(img_path)
        shutil.copy2(img_path, os.path.join(class_dir, img_name))
    
    return output_dir

def setup_classification_config(train_dir, val_dir, class_names, config_path):
    """
    Create YAML configuration for YOLO classification
    
    Args:
        train_dir (str): Path to organized training data directory
        val_dir (str): Path to organized validation data directory
        class_names (list): List of class names
        config_path (str): Path where to save the YAML config
    """
    # Convert to absolute paths
    train_dir = os.path.abspath(train_dir)
    val_dir = os.path.abspath(val_dir)
    
    data_yaml = {
        'path': os.path.dirname(train_dir),  # Base path for relative references
        'train': os.path.join(train_dir),  # Full path to train directory
        'val': os.path.join(val_dir),      # Full path to val directory
        'nc': len(class_names),
        'names': class_names
    }
    
    # Save YAML configuration
    with open(config_path, 'w') as f:
        yaml.dump(data_yaml, f, default_flow_style=False)


labels = [x.split('/')[-2] for x in files]

train_dir = prepare_classification_data(
        np.array(files)[train_idx],
        np.array(labels)[train_idx],
        '/eagle/FoundEpidem/astroka/yolo/huvec_control_seg_1/data/dataset/train'
    )
    
val_dir = prepare_classification_data(
    np.array(files)[test_idx],
    np.array(labels)[test_idx],
    '/eagle/FoundEpidem/astroka/yolo/huvec_control_seg_1/data/dataset/val'
)

# Define your class names
class_names = ['Compound_1', 'Compound_10', 'Compound_11', 'Compound_12',
       'Compound_13', 'Compound_14', 'Compound_15', 'Compound_16',
       'Compound_17', 'Compound_2', 'Compound_3', 'Compound_4',
       'Compound_5', 'Compound_6', 'Compound_7', 'Compound_8',
       'Compound_9', 'untreated']

# class_names = ['0.001', '0.01', '0.1', '1.0', '2.0', 'untreated']
# class_names = ['0.001', '0.1', '1.0', '2.0', 'untreated']
# class_names = ['0.001', '0.01', '0.1', '1.0', 'untreated']

# class_names = ['0.001', '0.01', '0.1', '1.0', '2.0']



# Setup configuration
setup_classification_config(
    train_dir=train_dir,
    val_dir=val_dir,
    class_names=class_names,
    config_path = '/eagle/FoundEpidem/astroka/yolo/huvec_control_seg_1/data/datasets/config.yaml'
    )

# g = glob.glob('/eagle/FoundEpidem/astroka/yolo/dataset/**/**/*.png')

# # print("G", g)

# #################
# #############

# Load a COCO-pretrained YOLO11n model
model = YOLO("yolo11x-cls.pt")


results = model.train(data="/eagle/FoundEpidem/astroka/yolo/huvec_control_seg_1/data/dataset/", epochs=100, imgsz=640, batch=24, patience=10, name='huvec_control_seg_1', classes= ['Compound_1', 'Compound_10', 'Compound_11', 'Compound_12','Compound_13', 'Compound_14', 'Compound_15', 'Compound_16', 'Compound_17', 'Compound_2', 'Compound_3', 'Compound_4', 'Compound_5', 'Compound_6', 'Compound_7', 'Compound_8', 'Compound_9', 'untreated'])
# results = model.train(data="/eagle/FoundEpidem/astroka/yolo/huvec_rad_seg_1/data/dataset/", epochs=100, imgsz=640, batch=24, patience=10, name='huvec_rad_seg_1', classes= ['0.001', '0.01', '0.1', '1.0', '2.0', 'untreated'])


# import torch
# print(results)
# print(" ")
# print(" ")
# print(" ")
# for result in results:
# embeddings = results.embeddings
# print(embeddings)
    # print("EMBEDDINGS", embeddings)
# print(results.boxes)
# for idx, layer in enumerate(model.model.children()):
#     print(f"Layer {idx}: {layer}")

# def get_intermediate_features(model, img, layer_idx=1):  # Layer before classification
#     features = []
    
#     def hook_fn(module, input, output):
#         features.append(output)

#     handle = list(model.model.children())[layer_idx].register_forward_hook(hook_fn)

#     img = torch.tensor(img).unsqueeze(0)  # Add batch dimension if needed
#     model(img)

#     handle.remove()
#     return features[0]

# img = "/eagle/FoundEpidem/astroka/yolo/rpe_rad_seg_2/images/2.0/r07c02f02p05_e4496946-0e6e-4082-8119-b1d0cf5f548e.png"  # Path to an image
# extracted_features = get_intermediate_features(model, img)
# print(" ")
# print(" ")

# print(" ")

# print("EXTRACTED FEATURES SHAPE")
# print(" ")

# print(" ")

# print(" ")

# print(extracted_features.shape)  # Feature tensor dimensions




