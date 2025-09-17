"""
Alexandros Papagiannakis, 2025, MIT license
"""

import nd2
from dataclasses import asdict
import numpy as np

def nd2_to_array(nd2_path):
    with nd2.ND2File(nd2_path) as f:
        iter_axis = f.sizes

        image_array = np.asarray(f)
        print(iter_axis)
        
        f.open()
        metdata = f.metadata
        f.close()
        metadata_dict = asdict(metdata)
    
    return image_array, iter_axis, metadata_dict


def raise_error_if_zero_dim(image_array):
    
    if any(s == 0 for s in image_array.shape):
        raise ValueError(f"Invalid array shape {image_array.shape}, zero dimension found.")
    else:
        print(f"Array shape {image_array.shape} is valid, no zero dimensions found.")




