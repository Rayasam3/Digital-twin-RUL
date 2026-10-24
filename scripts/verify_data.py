import pandas as pd

cols = (["unit", "cycle"]
        + [f"op{i}" for i in range(1, 4)]
        + [f"s{i}" for i in range(1, 22)])

df = pd.read_csv("data/raw/train_FD001.txt", sep=r"\s+", header=None, names=cols)

print("Shape   :", df.shape)
print("Engines :", df["unit"].nunique())
print("Longest life (cycles):", df.groupby("unit")["cycle"].max().max())
print(df.head())