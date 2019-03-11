import numpy as np
import pandas as pd


state = 0
x = 0
y1 = ''
y2 = ''
df_x = []
df_y1 = []
df_y2 = []

f = open("out_put.txt", "r")
data = f.read()

for d in data:
    if d == '(':
        state = 11
        x = x + 1
    elif d == ',':
        state = 22
    elif d == ')':
        state = 3
    else:
        pass

    if state == 1:
        y1 = y1 + d
    if state == 2:
        y2 = y2 + d
    if state == 3:
        y1 = float(y1)
        y2 = float(y2)
        state = 4
    if state == 4:
        df_x.append(x)
        df_y1.append(y1)
        df_y2.append(y2)
        # reset
        y1 = ''
        y2 = ''
        state = 0

    if state == 11:
        state = 1
    if state == 22:
        state = 2

data_df = {'x': df_x, 'y1': df_y1, 'y2': df_y2}
df = pd.DataFrame(data=data_df)
df.to_csv('output_align.csv', index=False)
