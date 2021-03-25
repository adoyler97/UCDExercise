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