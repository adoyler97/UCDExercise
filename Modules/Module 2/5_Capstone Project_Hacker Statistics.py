# Imagine the following: you're walking up the empire state building and you're playing a game with a friend.
# You throw a die one hundred times. If it's 1 or 2 you'll go one step down.If it's 3, 4, or 5, you'll go one step up.
# If you throw a 6, you'll throw the die again and will walk up the resulting number of steps.
# You have a 0.1% chance of tripping anf falling back to step 0
# You need to figure out the chance of winning before making a bet that you will get to step 60
# This code finds the percentage value and prints a histogram of results along with a visualisation of each trial
import numpy as np
import matplotlib.pyplot as plt

# Simulate random walk 500 times
all_walks = []
for i in range(1000):
    random_walk = [0]
    for x in range(100):
        step = random_walk[-1]
        dice = np.random.randint(1, 7)
        if dice <= 2:
            step = max(0, step - 1)
        elif dice <= 5:
            step = step + 1
        else:
            step = step + np.random.randint(1, 7)
        if np.random.rand() <= 0.001:
            step = 0
        random_walk.append(step)
    all_walks.append(random_walk)

# Create and plot np_aw_t
np_aw_t = np.transpose(np.array(all_walks))

# Select last row from np_aw_t: ends
ends = np_aw_t[-1, :]

# Plot histogram of ends, display plot
mean_result = round(np.mean(ends))
median_result = round(np.median(ends))
print("The percentage of trials that were above 60 steps was " + str(100 * sum(ends >= 60)/1000) + "%.")
print("The mean step reached was " + str(mean_result) + ".")
print("The median step reached was " + str(median_result) + ".")
plt.hist(ends)
plt.show()
plt.plot(np_aw_t)
plt.show()
