import pandas as pd

df = pd.read_parquet("aime_2024_problems.parquet")
df.to_csv('out.csv', index=False)
print(df)