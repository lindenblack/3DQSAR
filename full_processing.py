import os
import sys
import pandas as pd
import numpy as  np
import time
import os
import shutil
import subprocess

def set_globals():
    
    global open3D_directory
#     global dataset_name_num
#     global MIF_nodes 
#     global xyz_offset
    open3D_directory = "C:\open3dtools"
    
# set_globals(name = "3zyu",
#             nodes= [29,26,34],
#             offset = [33,14,21])

def agrd_to_array(entry_path,xyz_offset,dataset_name_num,MIF_nodes):
    fin = open(entry_path, "rt")
    fout = open("out.txt", "wt")

    for line in fin:
        fout.write(' '.join(line.split()))
        fout.write("\n")

    fin.close()
    fout.close()  
    npdata = np.loadtxt("out.txt",skiprows=5,delimiter=" ")
    MIF = np.zeros(MIF_nodes)
    for line in npdata:
        
        x,y,z,target = line
        x -= xyz_offset[0]
        y -= xyz_offset[1]
        z -= xyz_offset[2]
        MIF[int(x),int(y),int(z)] = target
    dataset_name = entry_path[15:].split("_")[0]
    number = entry_path[:-5].split("-")[-1]
    field = entry_path.split("_")[1]
    new_path =str(number+"_"+field+'.npy')    
    np.save(f"C:/Users/Linden/GitHub/3DQSAR/data/EllenMIF/{dataset_name_num}/{new_path}", MIF)

def process_dataset(xyz_offset,dataset_name_num,MIF_nodes):
    parent_dir = r"C:\Users\Linden\GitHub\3DQSAR\data\EllenMIF"
    new_dir_path = os.path.join(parent_dir, dataset_name_num)
    
    os.mkdir(new_dir_path)
    
    for entry in os.scandir(open3D_directory):
        if (entry.path.endswith(".agrd")):
            name = entry.path
            agrd_to_array(name,xyz_offset,dataset_name_num,MIF_nodes)    

def generate_labels():
    path = os.path.join(r"C:\Users\Linden\GitHub\3DQSAR\data\DatasetsEdited",dataset_name_num)
    tr = pd.read_csv(os.path.join(path,"pIC50.tr.txt"),
                     header=None,
                     delimiter=" ",
                     names=["Name","Y"],
                     index_col=False)
    
    if os.path.isfile(os.path.join(path,"pIC50.ts.txt")) == True:
        ts = pd.read_csv(os.path.join(path,"pIC50.ts.txt"),
                         header=None,
                         delimiter=" ",
                         names=["Name","Y"],
                         index_col=False)
        
        Y = pd.concat([tr,ts],ignore_index=True)
    else:
        Y = tr
    Y.sort_values(by=['Name'],inplace=True,ignore_index=True)
    count = len(Y)
    Y['ID']=np.arange(1,count+1)
    Y.to_csv(path_or_buf = os.path.join("data/LabelledData/",
                                        dataset_name_num,
                                        "pIC50.csv"),
             index=False)

def func():
    ds_num=0
    for entry in os.scandir(r"C:\Users\Linden\GitHub\3DQSAR\data\EllenRawData\sdf"):
        if (entry.path.endswith(".sdf")):
            
            file = open(r"C:\open3dtools\file.txt", "r")

            for line in file:
                line1=(line.split("\\"))
                old_name = line1[-1][:-6]
                break
            file.close()
            
            new_file_name = entry.name[:-4]
            
        
            dataset_name_num = new_file_name
            
            
            file = open(r"C:\open3dtools\file.txt", "r")
            new_file_content = ""
            itr=0
            for line in file:
                stripped_line = line.strip()
                new_line = stripped_line.replace(old_name, new_file_name)
                new_file_content += new_line +"\n"
              
            file.close()

            writing_file = open(r"C:\open3dtools\file.txt", "w")
            writing_file.write(new_file_content)
            writing_file.close()
            
            

            subprocess.run(['open3dqsar',
                            '-i',
                            'C:/open3dtools/file.txt'])
            
            print(f"agrd for DS num: {ds_num} generated")
            
           

            
            
            file = open(r"C:\open3dtools\therm_fld-01_obj-01.agrd", "r")
            lines=[]
            itr=0
            for line in file:
                lines.append(line)
                itr+=1
                if itr==6:
                    break
            file.close()
            MIF_nodes = [int(float(lines[4].split(":")[-1].replace(" ", "").split(",")[0])),
                         int(float(lines[4].split(":")[-1].replace(" ", "").split(",")[1])),
                         int(float(lines[4].split(":")[-1].replace(" ", "").split(",")[2][:-1]))
                        ]
            print(MIF_nodes)
            x_offset = int(float(lines[0].split(":")[-1].replace(" ", "").split(",")[0]))
            y_offset = int(float(lines[1].split(":")[-1].replace(" ", "").split(",")[0]))
            z_offset = int(float(lines[2].split(":")[-1].replace(" ", "").split(",")[0]))
            xyz_offset=[x_offset,y_offset,z_offset]
            
            
            set_globals()
            process_dataset(xyz_offset,dataset_name_num,MIF_nodes)
#             generate_labels()
            print(f"npy for DS num: {ds_num} generated")
            ds_num+=1

if __name__=="__main__":
    func()
 
