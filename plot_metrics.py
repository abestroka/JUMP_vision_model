import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Read the CSV file into a pandas DataFrame
df = pd.read_csv("/Users/abestroka/Argonne/git_repos/JUMP_vision_model/metrics.csv")


# Step 2: Interpolate missing values
df = df.interpolate(method='linear')

# Step 3: Create subplots and plot validation accuracy and validation loss
fig, ax1 = plt.subplots(figsize=(10, 5))

# Plot validation accuracy on the first subplot
color = 'tab:blue'
ax1.set_xlabel('Epoch')
ax1.set_ylabel('Validation Accuracy', color=color)
ax1.plot(df['epoch'], df['val_acc'], label='Validation Accuracy', color=color)
ax1.tick_params(axis='y', labelcolor=color)

# Create a second y-axis for validation loss
ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Validation Loss', color=color)
ax2.plot(df['epoch'], df['val_loss'], label='Validation Loss', color=color)
ax2.tick_params(axis='y', labelcolor=color)

# Add title and legend
fig.tight_layout()
plt.title('Validation Metrics', pad=20)
plt.grid(True)
plt.tight_layout()
plt.show()
