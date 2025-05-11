# data_pipeline.py

import pandas as pd
import os

# List of CSV files (manually downloaded from Football-Data.co.uk)
csv_files = ['raw_data/1516.csv', 'raw_data/1617.csv', 'raw_data/1718.csv', 'raw_data/1819.csv', 'raw_data/1920.csv', 'raw_data/2021.csv', 'raw_data/2122.csv',  'raw_data/2223.csv', 'raw_data/2324.csv', 'raw_data/l2425.csv']

COLUMNS_TO_KEEP = [
    'Date', 'HomeTeam', 'AwayTeam',
    'FTHG', 'FTAG', 'FTR',
    'HS', 'AS',  # Home/Away Shots
    'HST', 'AST',  # Shots on Target
    'HC', 'AC',  # Corners
    'HF', 'AF',  # Fouls committed
    'HY', 'AY',  # Yellow cards
    'HR', 'AR',  # Red cards
]

all_matches = []
for file in csv_files:
    if not os.path.exists(file):
        print(f"File not found: {file}")
        continue
    df = pd.read_csv(file)
    
    df = df[[col for col in COLUMNS_TO_KEEP if col in df.columns]].copy()
    
    all_matches.append(df)

df_all = pd.concat(all_matches, ignore_index=True)

porto_df = df_all[(df_all['HomeTeam'] == 'Porto') | (df_all['AwayTeam'] == 'Porto')].copy()

porto_df.rename(columns={
    'FTHG': 'HomeGoals',
    'FTAG': 'AwayGoals',
    'FTR': 'Result',
    'HS': 'HomeShots', 'AS': 'AwayShots',
    'HST': 'HomeShotsOnTarget', 'AST': 'AwayShotsOnTarget',
    'HC': 'HomeCorners', 'AC': 'AwayCorners',
    'HF': 'HomeFouls', 'AF': 'AwayFouls',
    'HY': 'HomeYellows', 'AY': 'AwayYellows',
    'HR': 'HomeReds', 'AR': 'AwayReds',
}, inplace=True)

porto_df['Date'] = pd.to_datetime(porto_df['Date'], dayfirst=True, errors='coerce')

porto_df = porto_df.dropna(subset=['Date'])

porto_df.to_csv('common/porto_matches.csv', index=False)

print(f"Total FC Porto matches: {len(porto_df)}")
print("Sample rows:")
print(porto_df.head())
