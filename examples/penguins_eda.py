"""EDA example for penguins data
"""
import pandas as pd

import shellplot as plt

pd.set_option("plotting.backend", "shellplot")
df = plt.load_dataset("penguins")


df["species"].value_counts().plot.barh()

df[["species", "island"]].value_counts().plot.barh()


df["body_mass_g"].hist(bins=10)


plt.plot(df["bill_length_mm"], df["flipper_length_mm"], color=df["species"])


df.dropna().plot("bill_depth_mm", "body_mass_g", color="species")

df.loc[df["species"] == "Adelie"].dropna().plot(
    "bill_depth_mm", "body_mass_g", color="island"
)
