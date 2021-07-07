# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 14:03:35 2021

@author: LLR User
"""

import os
# import pandas as pd
import numpy as  np

def set_globals():
    global open3D_directory
    global dataset_name
    global MIF_nodes 
    global xyz_offset
    open3D_directory = "C:\\data\\brd4\\3u5l_agrd"
    dataset_name = "3u5l"
    MIF_nodes = [34,39,37]
    xyz_offset = [13,24,3]

def agrd_to_array(entry_path):
    fin = open(entry_path, "rt")
    fout = open("C:\\data\\brd4\\3u5l\\out.txt", "wt")

    for line in fin:
        fout.write(' '.join(line.split()))
        fout.write("\n")

    fin.close()
    fout.close()  
    npdata = np.loadtxt("C:\\data\\brd4\\3u5l\\out.txt",skiprows=5,delimiter=" ")
    MIF = np.zeros(MIF_nodes)
    for line in npdata:
        x,y,z,target = line
        x -= xyz_offset[0]
        y -= xyz_offset[1]
        z -= xyz_offset[2]
        MIF[int(x),int(y),int(z)] = target
        
    # dataset_name = entry_path[14:].split("_")[0]
    number = entry_path[:-5].split("_")[3][4:]
    field = entry_path.split("_")[2][4:]
    new_path = str(dataset_name+"_"+number+"_"+field+'.npy')
    np.save(f"C:\\data\\brd4\\{dataset_name}\\{new_path}", MIF)
    # np.save(f"data/LabelledData/{dataset_name_num}/{new_path}", MIF)

def process_dataset():
    
    # # parent_dir = r"C:\Users\Linden\GitHub\3DQSAR\data\LabelledData"
    # parent_dir = r"C:\\data\\brd4"
    # new_dir_path = os.path.join(parent_dir, dataset_name)
    # os.mkdir(new_dir_path)
    
    entries = []
    
    for entry in os.scandir(open3D_directory):
        entries.append(entry)
        
        for entry in entries[::2]:
            
            if (entry.path.endswith(".agrd")):
                name = entry.path
                agrd_to_array(name)

# def generate_labels():
#     path = os.path.join(r"C:\Users\Linden\GitHub\3DQSAR\data\DatasetsEdited",dataset_name_num)
#     tr = pd.read_csv(os.path.join(path,"pIC50.tr.txt"),
#                      header=None,
#                      delimiter=" ",
#                      names=["Name","Y"],
#                      index_col=False)
    
#     if os.path.isfile(os.path.join(path,"pIC50.ts.txt")) == True:
#         ts = pd.read_csv(os.path.join(path,"pIC50.ts.txt"),
#                          header=None,
#                          delimiter=" ",
#                          names=["Name","Y"],
#                          index_col=False)
        
#         Y = pd.concat([tr,ts],ignore_index=True)
#     else:
#         Y = tr
    
#     Y.sort_values(by=['Name'],inplace=True,ignore_index=True)
#     count = len(Y)
#     Y['ID']=np.arange(1,count+1)
#     Y.to_csv(path_or_buf = os.path.join("data/LabelledData/",
#                                         dataset_name,
#                                         "pIC50.csv"),
#                                          index=False)

if __name__=="__main__":
    set_globals()
    process_dataset()
    # generate_labels()
