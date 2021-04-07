import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import time as time
from kaggle.api.kaggle_api_extended import KaggleApi
import zipfile

# Start time count to gauge process run time

start = time.time()
api = KaggleApi()
api.authenticate()

# downloading datasets for Chess games
api.dataset_download_files('arevel/chess-games')

# Read data in chunks of 100000 rows and concatenate into one dataframe at a time to speed up read time
zf = zipfile.ZipFile('chess-games.zip')
csv = pd.read_csv(zf.open('chess_games.csv'), chunksize=100000)
chess_df = pd.concat(csv)

# Show number of rows
print(chess_df.shape)

# Remove any duplicate values and fill N/A user names
chess_df = chess_df.drop_duplicates(subset=['White', 'Black'])

# show number of rows after dropping duplicates
print(chess_df.shape)
chess_df = chess_df.reset_index()

# Define average ELO rank per game
chess_df['AverageElo'] = (chess_df['WhiteElo'] + chess_df['BlackElo']) / 2

# Define chess rankings in ranges
# Super Grand Master = ELO 2700+
# Grand Master = 2500 - 2700
# IM_GM = 2400 - 2500
# FM_IM = 2300 - 2400
# CM_NM = 2200 - 2300
# Experts = 2000 - 2200
# Class_A = 1800 - 2000
# Class_B = 1600 - 1800
# Class_C = 1400 - 1600
# Class_D = 1200 - 1400
# Novices = 0 - 1200

# create lists of conditions
White_conditions = [(chess_df['WhiteElo'] >= 2700) &
                    (chess_df['WhiteElo'] <= 2700), (chess_df['WhiteElo'] >= 2500) &
                    (chess_df['WhiteElo'] <= 2500), (chess_df['WhiteElo'] >= 2400) &
                    (chess_df['WhiteElo'] <= 2400), (chess_df['WhiteElo'] >= 2300) &
                    (chess_df['WhiteElo'] <= 2300), (chess_df['WhiteElo'] >= 2200) &
                    (chess_df['WhiteElo'] <= 2200), (chess_df['WhiteElo'] >= 2000) &
                    (chess_df['WhiteElo'] <= 2000), (chess_df['WhiteElo'] >= 1800) &
                    (chess_df['WhiteElo'] <= 1800), (chess_df['WhiteElo'] >= 1600) &
                    (chess_df['WhiteElo'] <= 1600), (chess_df['WhiteElo'] >= 1400) &
                    (chess_df['WhiteElo'] <= 1400), (chess_df['WhiteElo'] >= 1200) &
                    (chess_df['WhiteElo'] <= 1200), (chess_df['WhiteElo'] >= 0)]

Black_conditions = [(chess_df['BlackElo'] >= 2700) &
                    (chess_df['BlackElo'] <= 2700), (chess_df['BlackElo'] >= 2500) &
                    (chess_df['BlackElo'] <= 2500), (chess_df['BlackElo'] >= 2400) &
                    (chess_df['BlackElo'] <= 2400), (chess_df['BlackElo'] >= 2300) &
                    (chess_df['BlackElo'] <= 2300), (chess_df['BlackElo'] >= 2200) &
                    (chess_df['BlackElo'] <= 2200), (chess_df['BlackElo'] >= 2000) &
                    (chess_df['BlackElo'] <= 2000), (chess_df['BlackElo'] >= 1800) &
                    (chess_df['BlackElo'] <= 1800), (chess_df['BlackElo'] >= 1600) &
                    (chess_df['BlackElo'] <= 1600), (chess_df['BlackElo'] >= 1400) &
                    (chess_df['BlackElo'] <= 1400), (chess_df['BlackElo'] >= 1200) &
                    (chess_df['BlackElo'] <= 1200), (chess_df['BlackElo'] >= 0)]

Average_conditions = [(chess_df['AverageElo'] >= 2700) &
                    (chess_df['AverageElo'] <= 2700), (chess_df['AverageElo'] >= 2500) &
                    (chess_df['AverageElo'] <= 2500), (chess_df['AverageElo'] >= 2400) &
                    (chess_df['AverageElo'] <= 2400), (chess_df['AverageElo'] >= 2300) &
                    (chess_df['AverageElo'] <= 2300), (chess_df['AverageElo'] >= 2200) &
                    (chess_df['AverageElo'] <= 2200), (chess_df['AverageElo'] >= 2000) &
                    (chess_df['AverageElo'] <= 2000), (chess_df['AverageElo'] >= 1800) &
                    (chess_df['AverageElo'] <= 1800), (chess_df['AverageElo'] >= 1600) &
                    (chess_df['AverageElo'] <= 1600), (chess_df['AverageElo'] >= 1400) &
                    (chess_df['AverageElo'] <= 1400), (chess_df['AverageElo'] >= 1200) &
                    (chess_df['AverageElo'] <= 1200), (chess_df['AverageElo'] >= 0)]

Outcome_conditions = [(chess_df['Result'] == "1-0") & (chess_df['Result'] == "0-1") &
                      (chess_df['Result'] == "1/2-1/2")]

# create a list of the values to assign for each condition
ELO = ['Super GM', 'GM', 'GM/IM', 'FM/IM', 'CM/NM', 'Experts', 'Class A', 'Class B', 'Class C', 'Class D', 'Novices']
Outcome = ['White Wins', 'Black Wins', 'Draw']

# create a new column and use np.select to assign values to it using the lists as arguments
chess_df['WhiteEloRank'] = np.select(White_conditions, ELO)
chess_df['BlackEloRank'] = np.select(Black_conditions, ELO)
chess_df['AverageEloRank'] = np.select(Average_conditions, ELO)

# create dataframe for moves
moves_df = chess_df["AN"].str.split(" ", n=30, expand=True)
moves_df = moves_df.drop(moves_df.iloc[:, 0:31:3], axis=1)

# append moves dataframe to chess dataframe
chess_df = pd.concat([chess_df, moves_df], axis=1)
chess_df.reset_index()
# chess_df['Outcome'] = np.select(Outcome_conditions, Outcome)
print(chess_df)

# sort data from lowest average ELO to highest average ELO
chess_df = chess_df.sort_values(by='AverageElo', ascending=False)
print(chess_df)

# Defining each game type in order to split dataframe into smaller sections for manipulation
Classical = ' Classical ', 'Classical '
Classical_Tournament = ' Classical tournament ', 'Classical tournament '
Blitz = ' Blitz ', 'Blitz '
Blitz_Tournament = ' Blitz tournament ', 'Blitz tournament '
Bullet = ' Bullet ', 'Bullet '
Bullet_Tournament = ' Bullet tournament ', 'Bullet tournament '
Correspondence = ' Correspondence ', 'Correspondence '

# Split chess dataframe into game type dataframes

Classical_df1 = chess_df[chess_df.Event == ' Classical ']
Classical_df2 = chess_df[chess_df.Event == 'Classical ']
Classical_df = pd.merge(Classical_df1, Classical_df2, how='outer')

Classical_Tournament_df1 = chess_df[chess_df.Event == ' Classical tournament ']
Classical_Tournament_df2 = chess_df[chess_df.Event == 'Classical tournament ']
Classical_Tournament_df = pd.merge(Classical_Tournament_df1, Classical_Tournament_df2, how='outer')

Blitz_df1 = chess_df[chess_df.Event == ' Blitz ']
Blitz_df2 = chess_df[chess_df.Event == 'Blitz ']
Blitz_df = pd.merge(Blitz_df1, Blitz_df2, how='outer')

Blitz_Tournament_df1 = chess_df[chess_df.Event == ' Blitz tournament ']
Blitz_Tournament_df2 = chess_df[chess_df.Event == 'Blitz tournament ']
Blitz_Tournament_df = pd.merge(Blitz_Tournament_df1, Blitz_Tournament_df2, how='outer')

Bullet_df1 = chess_df[chess_df.Event == ' Bullet ']
Bullet_df2 = chess_df[chess_df.Event == 'Bullet ']
Bullet_df = pd.merge(Bullet_df1, Bullet_df2, how='outer')

Bullet_Tournament_df1 = chess_df[chess_df.Event == ' Bullet tournament ']
Bullet_Tournament_df2 = chess_df[chess_df.Event == 'Bullet tournament ']
Bullet_Tournament_df = pd.merge(Bullet_Tournament_df1, Bullet_Tournament_df2, how='outer')

Correspondence_df1 = chess_df[chess_df.Event == ' Correspondence ']
Correspondence_df2 = chess_df[chess_df.Event == 'Correspondence ']
Correspondence_df = pd.merge(Correspondence_df1, Correspondence_df2, how='outer')

# Plot results
# fig, AvgElo, ax2, ax3, ax4 = plt.subplots()

# AvgElo.displot(Classical_df['AverageElo'], bins=50, kde=True)
# n ax2.displot(data=chess_df, x="AverageElo", hue="Termination", kind="hist")


# sns.displot(Correspondence_df['AverageElo'], bins=50, kde=True)
# sns.displot(data=chess_df, x="Termination", hue="Event", kind="kde")
# sns.displot(data=chess_df, x="AverageElo", hue="Termination", kind="hist")
# plt.show()
# plt.clf()

end = time.time()
print("Run Time: ", (end - start), 'Seconds')
