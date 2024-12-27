#!/usr/bin/env python3

import numpy as np
from scipy.spatial.distance import mahalanobis
from scipy.stats import chi2, kstest

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

# Analyze the distribution of Mahalanobis distances
mean_distance = np.mean(mahalanobis_distances)
std_distance = np.std(mahalanobis_distances)

print(f"Mean Mahalanobis Distance: {mean_distance}")
print(f"Standard Deviation of Mahalanobis Distances: {std_distance}")

# Perform the Kolmogorov-Smirnov test
ks_statistic, p_value = kstest(mahalanobis_distances, "chi2", args=(4,))
print(f"KS Statistic: {ks_statistic}")
print(f"P-Value: {p_value}")
