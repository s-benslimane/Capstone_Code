#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 23:12:15 2018

@author: mubarak
"""

import pandas as pd
import sqlite3
import math
connection = sqlite3.connect('clip_1.sqlite')
cursor = connection.cursor()

sql_command = "SELECT COUNT(*) FROM objects"
                   
max_objects_sql = cursor.execute(sql_command)
max_objects = max_objects_sql.fetchone()
    
object_df = pd.DataFrame()
for i in range(max_objects[0]):
    sql_command = "SELECT * FROM objects_features AS of \
                   JOIN positions \
                   USING (trajectory_id)\
                   WHERE object_id = "+str(i)+"\
                   ORDER BY object_id, trajectory_id"
                   
    join_obfeatures_positions = cursor.execute(sql_command)
    
    object_list = []
    
    for row in join_obfeatures_positions.fetchall():
        object_list.append(row)
    
    temp = pd.DataFrame(object_list)
    
    temp.rename(columns = {0:"object_id",1:"trajectory_id",2:"frame",3:"x_coords",4:"y_coords"},inplace = True)
    

    x_diff = (temp['x_coords'][temp.shape[0]-1]-temp['x_coords'][0])
    y_diff = (temp['y_coords'][temp.shape[0]-1]-temp['y_coords'][0])
    
#If you want to print the differences for every object, uncomment the two lines below    
# =============================================================================
#     print('Diff in X for '+ str(i) + ' is ' +str(x_diff))
#     print('Diff in Y for '+ str(i) + ' is ' +str(y_diff))
#     print('\n\n')
# =============================================================================
    
    if abs(x_diff) > 10:
        temp['new_class'] = 1
    elif abs(y_diff) > 4:
        temp['new_class'] = 2    
    
    object_df = object_df.append(temp)
    

#print(object_df[object_df['new_class'].isnull()].object_id.unique())

print("The cars in this clip are:")
print(object_df[object_df['new_class']==1].object_id.unique())
print('\n')
print("The pedestrians in this clip are:")
print(object_df[object_df['new_class']==2].object_id.unique())



    #print('Diff in X for '+ str(i) + ' is ' + str((object_df['x_coords'][object_df.shape[0]-1]-object_df['x_coords'][0])))
    #print('Diff in Y for '+ str(i) + ' is ' + str((object_df['y_coords'][object_df.shape[0]-1]-object_df['y_coords'][0])))
    #print('\n\n')
    
    
   # print("The difference in X direction for object" + str(i) "is " + str(object_df['x_coords'][object_df.shape[0]-1] - object_df['x_coords'][0]))
    
   # print("The difference in Y direction for object" + str(i) "is " + str(object_df['y_coords'][object_df.shape[0]-1] - object_df['y_coords'][0]))

        