import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import cv2


from batchgenerators.augmentations.spatial_transformations import augment_spatial_2

#https://github.com/MIC-DKFZ/batchgenerators/blob/master/batchgenerators/augmentations/spatial_transformations.py#L309
def augment_array(in_data):
    from multiprocessing import freeze_support
    freeze_support()
    
    data = np.reshape(in_data,(in_data.shape[0],
                               1,
                               in_data.shape[1],
                               in_data.shape[2],
                               in_data.shape[3]))
    patch_size = [in_data.shape[1],in_data.shape[2],in_data.shape[3]]
    augmented_data,_=augment_spatial_2(data=data,
                                       seg=None,
                                       patch_size=patch_size,
                                       patch_center_dist_from_border=30,
                                       do_elastic_deform=True,
                                       deformation_scale=(0, 0.25),
                                       do_rotation=True,
                                       angle_x=(0, 2 * np.pi),
                                       angle_y=(0, 2 * np.pi),
                                       angle_z=(0, 2 * np.pi),
                                       do_scale=True,
                                       scale=(0.75, 1.25),
                                       border_mode_data='nearest',
                                       border_cval_data=0,
                                       order_data=3,
                                       border_mode_seg='constant',
                                       border_cval_seg=0,
                                       order_seg=0,
                                       random_crop=True,
                                       p_el_per_sample=0.5,
                                       p_scale_per_sample=0.5,
                                       p_rot_per_sample=0.5,
                                       independent_scale_for_each_axis=False,
                                       p_rot_per_axis = 0.5,
                                       p_independent_scale_per_axis = 0.5)
    
    augmented_data = np.reshape(augmented_data,(augmented_data.shape[0],
                                                augmented_data.shape[2],
                                                augmented_data.shape[3],
                                                augmented_data.shape[4]))
#     print(f"Input data shape: {in_data.shape}\nOutput data shape: {augmented_data.shape}")
    return augmented_data

def data_augmentation(X_1,X_2,Y,augment_repetitions):
    augmented_X_1 = []
    augmented_X_2 = []
    for itr in range(augment_repetitions): 
        augmented_data = augment_array(X_1)
        augmented_X_1.append(augmented_data)
        

    for itr in range(augment_repetitions): 
        augmented_data = augment_array(X_2)
        augmented_X_2.append(augmented_data)

    for array in augmented_X_1:
        X_1 = np.vstack([X_1,array])

    for array in augmented_X_2:
        X_2 = np.vstack([X_2,array])

    Y=np.tile(Y,augment_repetitions+1)
    
    return X_1, X_2, Y
