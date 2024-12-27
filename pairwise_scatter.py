#!/usr/bin/env python3

import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# Load the cleaned quaternion data
data = np.loadtxt("quaternions.txt")

# Convert the data into a pandas DataFrame for easier plotting
df = pd.DataFrame(data, columns=["h", "i", "j", "k"])

# Create pairwise scatter plots using seaborn
pairplot = sns.pairplot(df, diag_kind="kde", corner=True)

# Save the plot as an image
pairplot.savefig("pairwise_scatter.png", dpi=300)
print("Pairwise scatter plot saved as 'pairwise_scatter.png'")
