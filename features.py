# features.py

import pandas as pd
import pickle
from sklearn.model_selection import train_test_split

ROLLING_WINDOW = 5
TEAM_NAME = "Porto"

df = pd.read_csv("common/porto_matches.csv", parse_dates=["Date"])

df = df.sort_values("Date").reset_index(drop=True)

def extract_porto_view(row):
    if row["HomeTeam"] == TEAM_NAME:
        return pd.Series({
            "IsHome": 1,
            "Opponent": row["AwayTeam"],
            "GoalsFor": row["HomeGoals"],
            "GoalsAgainst": row["AwayGoals"],
            "ShotsFor": row["HomeShots"],
            "ShotsAgainst": row["AwayShots"],
            "Result": row["Result"]
        })
    else:
        return pd.Series({
            "IsHome": 0,
            "Opponent": row["HomeTeam"],
            "GoalsFor": row["AwayGoals"],
            "GoalsAgainst": row["HomeGoals"],
            "ShotsFor": row["AwayShots"],
            "ShotsAgainst": row["HomeShots"],
            "Result": row["Result"]
        })

porto_view = df.apply(extract_porto_view, axis=1)

df_feat = pd.concat([df[["Date"]], porto_view], axis=1)

df_feat["Outcome"] = df_feat["Result"].map({"H": 2, "D": 1, "A": 0})  # 2=Win, 1=Draw, 0=Loss
if (df["HomeTeam"] != TEAM_NAME).iloc[0]:
    df_feat["Outcome"] = df_feat["Outcome"].map({2: 0, 0: 2, 1: 1})

for stat in ["GoalsFor", "GoalsAgainst", "ShotsFor", "ShotsAgainst"]:
    df_feat[f"{stat}_avg_{ROLLING_WINDOW}"] = (
        df_feat[stat]
        .shift(1)
        .rolling(ROLLING_WINDOW, min_periods=1)
        .mean()
    )

df_feat["Win"] = df_feat["Outcome"].apply(lambda x: 1 if x == 2 else 0)
df_feat["WinRate_5"] = df_feat["Win"].shift(1).rolling(ROLLING_WINDOW, min_periods=1).mean()
df_feat.drop(columns=["Win"], inplace=True)
df_feat = df_feat.dropna().reset_index(drop=True)

print("Sample engineered features:")
print(df_feat.head())

df = df_feat

columns_to_drop = ["Date", "Opponent", "GoalsFor", "GoalsAgainst", "Result", "Outcome"]
X = df.drop(columns=[col for col in columns_to_drop if col in df.columns])
y = df["Outcome"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

with open("data/X_train.pkl", "wb") as f:
    pickle.dump(X_train, f)
with open("data/X_test.pkl", "wb") as f:
    pickle.dump(X_test, f)
with open("data/y_train.pkl", "wb") as f:
    pickle.dump(y_train, f)
with open("data/y_test.pkl", "wb") as f:
    pickle.dump(y_test, f)