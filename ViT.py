import pandas as pd
import os
import random
import string
import shutil
import argparse
import numpy as np
import boto3
from botocore import UNSIGNED
from botocore.config import Config

# mura model imports
import requests
import math
import matplotlib.pyplot as plt
from getpass import getpass
from PIL import Image, UnidentifiedImageError
from requests.exceptions import HTTPError
from io import BytesIO
from pathlib import Path
import torch
import pytorch_lightning as pl
# from huggingface_hub import HfApi, HfFolder, Repository, notebook_login
from torch.utils.data import DataLoader
from torchmetrics import Accuracy
from torchvision.datasets import ImageFolder
# from transformers import ViTFeatureExtractor, ViTForImageClassification
from transformers import ViTImageProcessor, ViTForImageClassification


class ImageClassificationCollator:
    def __init__(self, feature_extractor):
        self.feature_extractor = feature_extractor
 
    def __call__(self, batch):
        encodings = self.feature_extractor([x[0] for x in batch], return_tensors='pt')
        encodings['labels'] = torch.tensor([x[1] for x in batch], dtype=torch.long)
        return encodings 

class Classifier(pl.LightningModule):

    def __init__(self, model, lr: float = 2e-5, **kwargs):
        super().__init__()
        self.save_hyperparameters('lr', *list(kwargs))
        self.model = model
        self.forward = self.model.forward
        self.val_acc = Accuracy(
            task='multiclass' if model.config.num_labels > 2 else 'binary',
            num_classes=model.config.num_labels
        )

    def training_step(self, batch, batch_idx):
        outputs = self(**batch)
        self.log(f"train_loss", outputs.loss)
        return outputs.loss

    def validation_step(self, batch, batch_idx):
        outputs = self(**batch)
        self.log(f"val_loss", outputs.loss)
        acc = self.val_acc(outputs.logits.argmax(1), batch['labels'])
        self.log(f"val_acc", acc, prog_bar=True)
        return outputs.loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.hparams.lr)
    



def ViT(cells_path):
    #init dataset, split into training and validation
    ds = ImageFolder(cells_path)
#     print(ds)
    indices = torch.randperm(len(ds)).tolist()
#     print(indices)
    n_val = math.floor(len(indices) * .15)
#     print(n_val)
    train_ds = torch.utils.data.Subset(ds, indices[:-n_val])
#     print(len(train_ds))
    val_ds = torch.utils.data.Subset(ds, indices[-n_val:])
#     print(len(val_ds))
    
    label2id = {}
    id2label = {}

    for i, class_name in enumerate(ds.classes):
        label2id[class_name] = str(i)
        id2label[str(i)] = class_name

    
    feature_extractor = ViTImageProcessor.from_pretrained('google/vit-base-patch16-224-in21k')
    model = ViTForImageClassification.from_pretrained(
        'google/vit-base-patch16-224-in21k',
        num_labels=len(label2id),
        label2id=label2id,
        id2label=id2label
    )
    collator = ImageClassificationCollator(feature_extractor)
    train_loader = DataLoader(train_ds, batch_size=8, collate_fn=collator, num_workers=0, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=8, collate_fn=collator, num_workers=0)

    pl.seed_everything(42)
    classifier = Classifier(model, lr=2e-5)
    trainer = pl.Trainer(accelerator="gpu", devices=-1, precision=16, max_epochs=16)
    # trainer = pl.Trainer(accelerator='mps', devices=1, precision=16, max_epochs=4)
    # trainer = pl.Trainer()
    trainer.fit(classifier, train_loader, val_loader)


def main():
    cells_path = '/eagle/projects/FoundEpidem/astroka/top_10/segmented_images'
    ViT(cells_path)

if __name__ == "__main__":
    main()


