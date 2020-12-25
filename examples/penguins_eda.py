"""EDA example for penguins data
"""
import pandas as pd

import shellplot as plt

pd.set_option("plotting.backend", "shellplot")
df = plt.load_dataset("penguins")


df["body_mass_g"].hist(figsize=(60, 20))

df["species"].value_counts().plot.barh(figsize=(30, 13))


# df[["island", "species"]].value_counts().plot.barh(figsize=(30, 30))

df.boxplot(column=["bill_length_mm", "bill_depth_mm"], figsize=(80, 13))

df.boxplot(column=["bill_length_mm"], by="species", figsize=(30, 13))

df.dropna().plot(
    "bill_length_mm", "flipper_length_mm", color="species", figsize=(40, 23)
)

# df.loc[df["species"] == "Adelie"].dropna().plot(
#     "bill_depth_mm", "body_mass_g", color="island"
# )
