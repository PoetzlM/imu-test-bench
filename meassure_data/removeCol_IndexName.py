# -*- coding: utf-8 -*-
"""
Created on Wed May 18 06:50:09 2022

@author: PoetzlM
"""

import pandas as pd

df1 = pd.read_csv("meanListAccel.csv", index_col=0)
df1.to_csv("meanListAccel.csv", index = False, header = False)

print(df1.head(10))

df2 = pd.read_csv("meanListGyro.csv", index_col=0)
df2.to_csv("meanListGyro.csv", index = False, header = False)

print(df2.head(10))

df3 = pd.read_csv("meanMagList.csv", index_col=0)
df3.to_csv("meanMagList.csv", index = False, header = False)

print(df3.head(10))
