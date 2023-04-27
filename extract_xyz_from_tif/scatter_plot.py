import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('./level_location.csv', usecols=['LAT', 'LON', 'VALUE_levelling','value_InSAR'])
x = df['VALUE_levelling']
y = df['value_InSAR']

plt.scatter(x, y)
plt.show()
