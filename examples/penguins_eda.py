"""EDA example for penguins data
"""
import pandas as pd

import shellplot as plt

pd.set_option("plotting.backend", "shellplot")
df = plt.load_dataset("penguins")


df["body_mass_g"].hist()

df[["species", "island"]].value_counts().plot.barh()

df.boxplot(column=["bill_length_mm", "bill_depth_mm"])

df.boxplot(column=["bill_length_mm"], by="species")

df.dropna().plot("bill_length_mm", "flipper_length_mm", color="species")


# df.loc[df["species"] == "Adelie"].dropna().plot(
#     "bill_depth_mm", "body_mass_g", color="island"
# )
