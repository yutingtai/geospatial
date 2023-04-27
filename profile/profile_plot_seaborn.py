import matplotlib.pyplot as plt
import pandas as pd
import seaborn

df = pd.read_csv('./displacement_2.csv')
x = df['time']
x1 = [int(i) for i in range(20)]

y1 = df['TK172']  # 第一組的 Y 軸數據
y2 = df['temple']  # 第二組的 Y 軸數據

#fig = plt.figure(figsize=(12, 3))


ax1 = seaborn.regplot(data=None, x=x1, y=y1, order=1, logistic=False, lowess=False, robust=False, logx=False, color=None,
                marker='o', label='TK172')
seaborn.regplot(data=None, x=x1, y=y2, order=1, logistic=False, lowess=False, robust=False, logx=False, color=None,
                marker='+', label='temple')



plt.gcf().autofmt_xdate()
plt.legend()
plt.show()
