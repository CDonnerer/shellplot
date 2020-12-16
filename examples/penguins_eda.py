"""EDA example for penguins data
"""
import numpy as np
import pandas as pd

import shellplot as plt

pd.set_option("plotting.backend", "shellplot")
df = plt.load_dataset("penguins")


x = np.arange(-3, 3, 0.01)
y = np.cos(x) ** 2

plt.plot(x, y)

df["bill_length_mm"].hist(bins=14)

plt.plot(df["bill_length_mm"], df["flipper_length_mm"], color=df["species"])

plt.plot(df["bill_depth_mm"], df["body_mass_g"], color=df["species"])


df["species"].value_counts().plot.barh()
