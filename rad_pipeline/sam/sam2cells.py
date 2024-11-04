import torch
from sam2 import Sam2Model  # Import SAM2 model
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
from torchvision.datasets import ImageFolder

# Load dataset
data_dir = "/eagle/FoundEpidem/astroka/fib_and_htert/week_one/results/fib_control"
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])
dataset = ImageFolder(root=data_dir, transform=transform)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

# Initialize model
model = Sam2Model(pretrained=True)
model.train()  # Set model to training mode

# Define optimizer and loss function
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Training loop
for epoch in range(num_epochs):
    for images, labels in dataloader:
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

# After training, use model.eval() for inference
model.eval()
