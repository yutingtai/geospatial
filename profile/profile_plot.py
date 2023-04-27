import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd



df = pd.read_csv('./displacement_2.csv')
x = df['time']
x1 = df['date_int']


y1 = df['TK172']   # 第一組的 Y 軸數據
y2 = df['temple']  # 第二組的 Y 軸數據

fig = plt.figure(figsize=(12,3))
plt.scatter(x1, y1, c='b', label='TK172')
plt.scatter(x1, y2, c='r', label='temple')

m_tk172, b_tk172 = np.polyfit(x1, y1, 1)
#m_temple, b_temple = np.polyfit(x1,y2,1)


#add linear regression line to scatterplot
plt.plot(x1, m_tk172*x1+b_tk172,color='blue')
#plt.plot(x1, m_temple*x1+b_temple,color = 'red')

ax = plt.gca()
ax.xaxis.set_major_locator(mdates.DayLocator(interval=20))
ax.xaxis.set_minor_locator(mdates.DayLocator())
plt.gcf().autofmt_xdate()
plt.legend()
plt.show()
