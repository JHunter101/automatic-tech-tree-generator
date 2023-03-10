# -*- coding: utf-8 -*-
"""
Automatic Tech Tree Generator
"""

import graphviz
import pandas as pd
import os
import numpy as np
os.chdir(os.path.dirname(os.path.realpath(__file__)))


def name_to_id(name):
    """Convert name to ID"""
    return ids[names.index(name)]

# Import tech tree data
df = pd.read_csv('tech_info.csv') 
df = df.applymap(str)

# Create Base
f = graphviz.Digraph(filename = "output/cycle 1.gv", graph_attr={
                                                                'label': 'Cycle 1 Tech Tree', 
                                                                'splines': 'ortho', 
                                                                'nodesep': '0.5', 
                                                                'ranksep': '0.5', 
                                                                'rankdir': 'LR', 
                                                                'overlap': 'prism', 
                                                                'overlap_scaling': '0.01', 
                                                                'ratio': '0.71'
                                                                 })

# Extract Base Information
ids = df['ID'].tolist()
names = df['Name'].tolist()
colors = df['C'].tolist()
for my_id, my_name, my_color in zip(ids, names, colors):
     f.node(my_id, my_name, color = my_color, shape = 'rounded')

# Create Connections
for index, row in df.iterrows():
    if row['Prerequisite 1'] == '-':
        continue
    else:
        for i in range(1,7):
            preStr = 'Prerequisite ' + str(i)
            pName = row[preStr]
            if pName != "nan":
                if pName in names:
                    pID = name_to_id(pName)
                else:
                    pID = str(int(ids[-1]) + 1)
                    ids.append(pID)
                    names.append(pName)
                    f.node(pID, pName, color = 'black', shape = 'rounded')
                
                if i <= 4:
                    f.edge(pID, row['ID'], style="filled", constraint = row['CS'])
                
                else:
                    f.edge(pID, row['ID'], style="dashed", constraint = row['CS'])
                    
f.view()
