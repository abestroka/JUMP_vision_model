import torch
import sys
# from sam2 import SamPredictor, build_sam_vit_h

from sam2.build_sam import build_sam2
from sam2.sam2_image_predictor import SAM2ImagePredictor

from PIL import Image
import tifffile
import numpy as np
import matplotlib.pyplot as plt

# Load the SAM model with the appropriate checkpoint
def load_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    # device = 'cpu'
    model_cfg = "configs/sam2.1/sam2.1_hiera_l.yaml"
    model = build_sam2(model_cfg, checkpoint="path/to/sam2/checkpoint.pth")  # specify the checkpoint path
    model.to(device)
    predictor = Sam2ImagePredictor(model)
    return predictor, device

# Load TIFF image file
def load_tiff_image(file_path):
    with tifffile.TiffFile(file_path) as tif:
        image = tif.asarray()
    # Ensure the image is in the correct format
    if len(image.shape) == 2:  # Grayscale image
        image = np.stack([image] * 3, axis=-1)  # Convert to RGB format for SAM if needed
    return image

# Run SAM to get masks for cells
def apply_masks(image, predictor, device):
    predictor.set_image(image)
    # Assume we want masks across the entire image without specifying points
    masks, _, _ = predictor.predict(
        point_coords=None,
        point_labels=None,
        box=None,
        mask_input=None,
        multimask_output=False,
    )
    return masks

# Display masks over the image
def display_masks(image, masks):
    plt.imshow(image)
    for mask in masks:
        plt.imshow(mask, alpha=0.5)  # Overlay each mask with transparency
    plt.axis('off')
    plt.show()

# Main function to load image, predict masks, and display
def main(file_path):
    predictor, device = load_model()
    image = load_tiff_image(file_path)
    masks = apply_masks(image, predictor, device)
    display_masks(image, masks)

# Provide the path to your TIFF file here
file_path = "/Users/abestroka/Argonne/LUCID/raw_week_3/r01c02f04p01-ch3sk1fk1fl1.tiff"
main(file_path)

