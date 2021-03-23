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

Classical_Tournament_df1 = chess_df[chess_df.Event == ' Classical tournament ']
Classical_Tournament_df2 = chess_df[chess_df.Event == 'Classical tournament ']
Classical_Tournament_df = pd.merge(Classical_Tournament_df1, Classical_Tournament_df2, how='outer')
print(Classical_Tournament_df)

Blitz_df1 = chess_df[chess_df.Event == ' Blitz ']
Blitz_df2 = chess_df[chess_df.Event == 'Blitz ']
Blitz_df = pd.merge(Blitz_df1, Blitz_df2, how='outer')
print(Blitz_df)

Blitz_Tournament_df1 = chess_df[chess_df.Event == ' Blitz tournament ']
Blitz_Tournament_df2 = chess_df[chess_df.Event == 'Blitz tournament ']
Blitz_Tournament_df = pd.merge(Blitz_Tournament_df1, Blitz_Tournament_df2, how='outer')
print(Blitz_Tournament_df)

Bullet_df1 = chess_df[chess_df.Event == ' Bullet ']
Bullet_df2 = chess_df[chess_df.Event == 'Bullet ']
Bullet_df = pd.merge(Bullet_df1, Bullet_df2, how='outer')
print(Bullet_df)

Bullet_Tournament_df1 = chess_df[chess_df.Event == ' Bullet tournament ']
Bullet_Tournament_df2 = chess_df[chess_df.Event == 'Bullet tournament ']
Bullet_Tournament_df = pd.merge(Bullet_Tournament_df1, Bullet_Tournament_df2, how='outer')
print(Bullet_Tournament_df)

Correspondence_df1 = chess_df[chess_df.Event == ' Correspondence ']
Correspondence_df2 = chess_df[chess_df.Event == 'Correspondence ']
Correspondence_df = pd.merge(Correspondence_df1, Correspondence_df2, how='outer')
print(Correspondence_df)

end = time.time()
print("Run Time: ", (end-start), 'Seconds')
