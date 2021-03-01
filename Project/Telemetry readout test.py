import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
low_memory = False

D0TelemetryDataSet = pd.read_csv("Driver 1 Telemetry.csv", dtype=object)

Column_names_list = list(D0TelemetryDataSet.columns)

# print(Column_names_list)

D0 = pd.DataFrame(D0TelemetryDataSet, columns=Column_names_list)
D0["gear"]=D0["gear"].astype(float)
D0["speed"]=D0["speed"].astype(float)
D0["lapDistance"]=D0["lapDistance"].astype(float)
# D0.speed = pd.to_numeric(D0.speed)
# D0.sessionTime = pd.to_numeric(D0.sessionTime)
Lap_Distance = D0.iloc[0:1874, 52:28]
Lap_1_Speed = D0.iloc[0:1874, 27:28]
Lap_2_speed = D0.iloc[1875:3455, 27:28]

# Lap_1_Speed.plot(x='lapDistance', y='speed', s=0.1, kind='scatter')
# Lap_2_speed.plot(x='lapDistance', y='speed', s=0.1, kind='scatter')
# Lap_1_Speed.ylabel('Speed (Kph)')
# Lap_1_Speed.xlabel('Lap Distance')
# Lap_2_speed.ylabel('Speed (Kph)')
# Lap_2_speed.xlabel('Lap Distance')

D0.plot(x='sessionTime', y='gear', kind='line')
D0.plot(x='sessionTime', y='speed', kind='line')
plt.ylabel('Speed (Kph)')
plt.xlabel('Lap Distance')

plt.show()