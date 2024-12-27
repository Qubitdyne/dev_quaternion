#!/usr/bin/env python3

import numpy as np

# Load the cleaned quaternion data
data = np.loadtxt("quaternions.txt")

# Calculate variances for each component
variances = np.var(data, axis=0)
print("Variances of Components (h, i, j, k):", variances)

# Calculate the correlation matrix
correlation_matrix = np.corrcoef(data, rowvar=False)
print("Correlation Matrix:\n", correlation_matrix)
