#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load the cleaned quaternion data
data = np.loadtxt("quaternions.txt")
h, i, j, k = data[:, 0], data[:, 1], data[:, 2], data[:, 3]

# Create a 3D scatter plot for h, i, j
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Scatter plot
scatter = ax.scatter(h, i, j, c=k, cmap='viridis', alpha=0.5)
colorbar = plt.colorbar(scatter, ax=ax, label='k component')

# Labels and title
ax.set_title("3D Scatter Plot of Quaternion Components")
ax.set_xlabel("h component")
ax.set_ylabel("i component")
ax.set_zlabel("j component")

#plt.show()

# Save the plot as a file
plt.savefig("quaternion_scatter_plot.png", dpi=300)
print("Scatter plot saved as 'quaternion_scatter_plot.png'")

