import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import time as time
from kaggle.api.kaggle_api_extended import KaggleApi
import zipfile


def chess_analysis():
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

    # Remove any duplicate user names to limit data to one game per user
    chess_df = chess_df.drop_duplicates(subset=['White', 'Black'])

    # remove any rows with stockfish evaluation as this clogs up the data at a later stage
    chess_df = chess_df.drop(chess_df[chess_df.AN.str.contains(r'[{}]')].index)

    # use iterrows to print out data
    for index, row in chess_df.head(1000).iterrows():
        print(index, row)

    # reset index after dropping duplicate users and removing stockfish evaluations
    chess_df = chess_df.reset_index()

    # Define average elo rank per game
    chess_df['AverageElo'] = (chess_df['WhiteElo'] + chess_df['BlackElo']) / 2

    # create lists of conditions to use for np.se;ect to add new columns to turn numeric values into grouped categories
    white_conditions = [(chess_df['WhiteElo'] > 2700),
                    (chess_df['WhiteElo'] < 2700) & (chess_df['WhiteElo'] >= 2500),
                    (chess_df['WhiteElo'] < 2500) & (chess_df['WhiteElo'] >= 2400),
                    (chess_df['WhiteElo'] < 2400) & (chess_df['WhiteElo'] >= 2300),
                    (chess_df['WhiteElo'] < 2300) & (chess_df['WhiteElo'] >= 2200),
                    (chess_df['WhiteElo'] < 2200) & (chess_df['WhiteElo'] >= 2000),
                    (chess_df['WhiteElo'] < 2000) & (chess_df['WhiteElo'] >= 1800),
                    (chess_df['WhiteElo'] < 1800) & (chess_df['WhiteElo'] >= 1600),
                    (chess_df['WhiteElo'] < 1600) & (chess_df['WhiteElo'] >= 1400),
                    (chess_df['WhiteElo'] < 1400) & (chess_df['WhiteElo'] >= 1200),
                    (chess_df['WhiteElo'] < 1200) & (chess_df['WhiteElo'] >= 0)]

    black_conditions = [(chess_df['BlackElo'] >= 2700),
                    (chess_df['BlackElo'] < 2700) & (chess_df['BlackElo'] >= 2500),
                    (chess_df['BlackElo'] < 2500) & (chess_df['BlackElo'] >= 2400),
                    (chess_df['BlackElo'] < 2400) & (chess_df['BlackElo'] >= 2300),
                    (chess_df['BlackElo'] < 2300) & (chess_df['BlackElo'] >= 2200),
                    (chess_df['BlackElo'] < 2200) & (chess_df['BlackElo'] >= 2000),
                    (chess_df['BlackElo'] < 2000) & (chess_df['BlackElo'] >= 1800),
                    (chess_df['BlackElo'] < 1800) & (chess_df['BlackElo'] >= 1600),
                    (chess_df['BlackElo'] < 1600) & (chess_df['BlackElo'] >= 1400),
                    (chess_df['BlackElo'] < 1400) & (chess_df['BlackElo'] >= 1200),
                    (chess_df['BlackElo'] < 1200) & (chess_df['BlackElo'] >= 0)]

    average_conditions = [(chess_df['AverageElo'] >= 2700),
                      (chess_df['AverageElo'] < 2700) & (chess_df['AverageElo'] >= 2500),
                      (chess_df['AverageElo'] < 2500) & (chess_df['AverageElo'] >= 2400),
                      (chess_df['AverageElo'] < 2400) & (chess_df['AverageElo'] >= 2300),
                      (chess_df['AverageElo'] < 2300) & (chess_df['AverageElo'] >= 2200),
                      (chess_df['AverageElo'] < 2200) & (chess_df['AverageElo'] >= 2000),
                      (chess_df['AverageElo'] < 2000) & (chess_df['AverageElo'] >= 1800),
                      (chess_df['AverageElo'] < 1800) & (chess_df['AverageElo'] >= 1600),
                      (chess_df['AverageElo'] < 1600) & (chess_df['AverageElo'] >= 1400),
                      (chess_df['AverageElo'] < 1400) & (chess_df['AverageElo'] >= 1200),
                      (chess_df['AverageElo'] < 1200) & (chess_df['AverageElo'] >= 0)]

    outcome_conditions = [(chess_df['Result']) == "1-0", (chess_df['Result']) == "0-1",
                          (chess_df['Result']) == "1/2-1/2", (chess_df['Result']) == "*"]

    # create a list of the values to assign for each condition
    elo = ['Super GM', 'GM', 'GM/IM', 'FM/IM', 'CM/NM', 'Experts', 'Class A', 'Class B', 'Class C', 'Class D',
           'Novices']
    outcome = ['White Wins', 'Black Wins', 'Draw', 'No Result']

    # create new columns and use np.select to assign values to it using the lists as arguments
    chess_df['WhiteEloRank'] = np.select(white_conditions, elo)
    chess_df['BlackEloRank'] = np.select(black_conditions, elo)
    chess_df['AverageEloRank'] = np.select(average_conditions, elo)
    chess_df['Outcome'] = np.select(outcome_conditions, outcome)

    # create dataframe for moves
    moves_df = chess_df["AN"].str.split(" ", n=30, expand=True)
    moves_df = moves_df.drop(moves_df.iloc[:, 0:31:3], axis=1)

    # append moves dataframe to chess dataframe
    chess_df = pd.concat([chess_df, moves_df], axis=1)
    chess_df.reset_index(inplace=True)

    # sort data from lowest average elo to highest average elo
    chess_df = chess_df.sort_values(by='AverageElo', ascending=False)

    # change data type from object to numeric values
    chess_df[["WhiteElo", "BlackElo", "AverageElo"]] = chess_df[["WhiteElo", "BlackElo", "AverageElo"]].\
        apply(pd.to_numeric)

    classical_df1 = chess_df[chess_df.Event == ' Classical ']
    classical_df2 = chess_df[chess_df.Event == 'Classical ']
    classical = pd.merge(classical_df1, classical_df2, how='outer')

    classical_tournament_df1 = chess_df[chess_df.Event == ' Classical tournament ']
    classical_tournament_df2 = chess_df[chess_df.Event == 'Classical tournament ']
    classical_tournament = pd.merge(classical_tournament_df1, classical_tournament_df2, how='outer')

    blitz_df1 = chess_df[chess_df.Event == ' Blitz ']
    blitz_df2 = chess_df[chess_df.Event == 'Blitz ']
    blitz = pd.merge(blitz_df1, blitz_df2, how='outer')

    blitz_tournament_df1 = chess_df[chess_df.Event == ' Blitz tournament ']
    blitz_tournament_df2 = chess_df[chess_df.Event == 'Blitz tournament ']
    blitz_tournament = pd.merge(blitz_tournament_df1, blitz_tournament_df2, how='outer')

    bullet_df1 = chess_df[chess_df.Event == ' Bullet ']
    bullet_df2 = chess_df[chess_df.Event == 'Bullet ']
    bullet = pd.merge(bullet_df1, bullet_df2, how='outer')

    bullet_tournament_df1 = chess_df[chess_df.Event == ' Bullet tournament ']
    bullet_tournament_df2 = chess_df[chess_df.Event == 'Bullet tournament ']
    bullet_tournament = pd.merge(bullet_tournament_df1, bullet_tournament_df2, how='outer')

    correspondence_df1 = chess_df[chess_df.Event == ' Correspondence ']
    correspondence_df2 = chess_df[chess_df.Event == 'Correspondence ']
    correspondence = pd.merge(correspondence_df1, correspondence_df2, how='outer')

    # Plot results
    #  Categorical Data
    plots = ['Termination', 'Outcome', 'AverageEloRank']
    plots_1 = ['AverageElo']
    plots_2 = [1, 2]
    game_types = [classical, classical_tournament, blitz, blitz_tournament, bullet, bullet_tournament, correspondence]
    game_types_str = ['Classical', 'Classical Tournament', 'Blitz', 'Blitz Tournament', 'Bullet', 'Bullet Tournament',
                      'Correspondence']

    z = 0
    y = 0
    w = 0
    for x in game_types:
        a = 1  # number of rows, set to 1 to retrieve individual graph groups based on game type
        b = int(len(plots))  # number of columns
        c = 1  # initialize plot counter
        d = 1  # number of rows, set to 1 to retrieve individual graph groups based on game type
        e = int(len(plots_1))  # number of columns
        f = 1  # initialize plot counter
        g = 1  # number of rows, set to 1 to retrieve individual graph groups based on game type
        h = int(len(plots_2))  # number of columns
        k = 1  # initialize plot counter
        for i in plots:
            plt.subplot(a, b, c)
            plt.title(str(game_types_str[z]))
            plt.xlabel(i)
            plt.subplots_adjust(bottom=0.095, top=0.97, hspace=1, wspace=0.45)
            sns.countplot(x=x[i])
            plt.xticks(rotation=30)
            c = c + 1
        z = z + 1
        plt.show()
        plt.clf()

        for i in plots_1:
            plt.subplot(d, e, f)
            plt.title(str(game_types_str[y]))
            plt.xlabel(i)
            plt.subplots_adjust(bottom=0.095, top=0.97, hspace=1)
            sns.histplot(x=x[i], kde=True, bins=25)
            plt.xticks(rotation=30)
            f = f + 1
        y = y + 1
        plt.show()
        plt.clf()
        for i in plots_2:
            plt.subplot(g, h, k)
            plt.title(str(game_types_str[w]))
            plt.xlabel(i)
            plt.subplots_adjust(bottom=0.095, top=0.97, hspace=1)
            sns.countplot(x=x[i])
            plt.xticks(rotation=30)
            k = k + 1
        w = w + 1
        plt.show()
        plt.clf()

    end = time.time()

    print("Run Time: ", (end - start), 'Seconds')


chess_analysis()
