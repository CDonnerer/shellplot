"""EDA example for penguins data
"""

import pandas as pd

import shellplot as plt

pd.set_option("plotting.backend", "shellplot")
df = plt.load_dataset("penguins")

# df["bill_length_mm"].hist(bins=20)

plt.plot(df["bill_length_mm"], df["flipper_length_mm"], color=df["species"])

df["species"].value_counts().plot.barh()
