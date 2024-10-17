import torch
import torch.nn as nn
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

transform = transforms.Compose([
    transforms.Resize((224, 224)),  # ResNet input size
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  # ImageNet mean and std
])

test_dataset = datasets.ImageFolder(root='/eagle/FoundEpidem/astroka/fib_and_htert/cnn_data/week_one/fib_rad', transform=transform)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

print("CLASSES")
print(test_dataset.class_to_idx)

print("")

num_classes = len(test_dataset.classes)
print(f"Number of classes: {num_classes}")
print(f"Class-to-index mapping: {test_dataset.class_to_idx}")


model = models.resnet50(pretrained=True)

# num_classes = 5

model.fc = nn.Linear(model.fc.in_features, num_classes)

model = model.to(device)
model.eval()  



correct = 0
total = 0

with torch.no_grad():
    for inputs, labels in test_loader:
        inputs, labels = inputs.to(device), labels.to(device)

        outputs = model(inputs)

        _, predicted = torch.max(outputs, 1)

        total += labels.size(0)
        correct += (predicted == labels).sum().item()


accuracy = 100 * correct / total
print(f'Accuracy of the pre-trained model on the test dataset: {accuracy:.2f}%')
