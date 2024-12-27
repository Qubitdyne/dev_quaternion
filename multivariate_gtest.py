#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

# Load the cleaned data
data = np.loadtxt("quaternions.txt")

# Extract components
h, i, j, k = data[:, 0], data[:, 1], data[:, 2], data[:, 3]

# Visualize 2D projections
plt.figure(figsize=(10, 6))
plt.scatter(h, i, alpha=0.5, label="h vs i")
plt.scatter(h, j, alpha=0.5, label="h vs j")
plt.scatter(i, j, alpha=0.5, label="i vs j")
plt.legend()
plt.title("2D Projections of Quaternion Components")
plt.xlabel("Component 1")
plt.ylabel("Component 2")
plt.grid()
plt.show()

# Check if the data is Gaussian in higher dimensions
mean = np.mean(data, axis=0)
covariance = np.cov(data, rowvar=False)

print("Mean:", mean)
print("Covariance Matrix:\n", covariance)

