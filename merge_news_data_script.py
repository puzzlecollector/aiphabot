import pandas as pd

df1 = pd.read_csv("tokenpost_V2_3200.csv")
df2 = pd.read_csv("coinness_full_2306.csv")

print(df1)

print()
print()

print(df2)

print()
print()

merged_df = pd.concat([df1, df2])
merged_df["datetimes"] = pd.to_datetime(merged_df["datetimes"])
sorted_df = merged_df.sort_values(by="datetimes")
clean_df = sorted_df.drop_duplicates()

print(clean_df)


clean_df.to_csv("coinness_20240602.csv", index=False)
