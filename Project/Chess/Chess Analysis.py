import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import time as time

start = time.time()
# Read data in chunks of 100000 rows at a time to speed up read time
chess = pd.read_csv('chess_games.csv', chunksize=100000)
chess_df = pd.concat(chess)

column_names = chess_df.columns
game_types = chess_df['Event'].unique().tolist()
print(game_types)

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
print(Classical_df)

super_GM = range(2700, 4000)
GM = range(2500, 2700)
IM_GM = range(2400, 2500)
FM_IM = range(2300, 2400)
CM_NM = range(2200, 2300)
Experts = range(2000, 2200)
Class_A = range(1800, 2000)
Class_B = range(1600, 1800)
Class_C = range(1400, 1600)
Class_D = range(1200, 1400)
Novices = range(0, 1200)

ELOBands = [GM, IM_GM, FM_IM, CM_NM, Experts, Class_A, Class_B, Class_C, Class_D, Novices]

Classical_df['WhiteElo'] = Classical_df['WhiteElo'].isin(ELOBands).any()
Classical_df['BlackELO'] = Classical_df['BlackElo'].isin(ELOBands).any()
print(Classical_df)

# fig, ax = plt.subplots()

# ax.bar(Classical_df[""], Classical_df[""])

end = time.time()
print("Run Time: ", (end-start), 'Seconds')
