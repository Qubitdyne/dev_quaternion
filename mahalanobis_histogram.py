#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import mahalanobis
from scipy.stats import chi2

# Load the cleaned quaternion data
data = np.loadtxt("quaternions.txt")

# Calculate mean and covariance matrix
mean_vector = np.mean(data, axis=0)
cov_matrix = np.cov(data, rowvar=False)

# Inverse of the covariance matrix for Mahalanobis distance
cov_matrix_inv = np.linalg.inv(cov_matrix)

# Compute Mahalanobis distances for all points
mahalanobis_distances = np.array([
    mahalanobis(point, mean_vector, cov_matrix_inv)
    for point in data
])

# Plot histogram of Mahalanobis distances
plt.hist(mahalanobis_distances, bins=30, density=True, alpha=0.6, label="Mahalanobis Distances")

# Overlay the chi-squared distribution
x = np.linspace(0, 8, 100)
plt.plot(x, chi2.pdf(x, df=4), label="Chi-Squared (df=4)", color='red')

# Plot settings
plt.title("Mahalanobis Distances vs Chi-Squared Distribution")
plt.xlabel("Mahalanobis Distance")
plt.ylabel("Density")
plt.legend()
plt.grid()

# Save the plot as an image
plt.savefig("mahalanobis_histogram.png", dpi=300)
print("Histogram saved as 'mahalanobis_histogram.png'")
