# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 13:10:09 2024

@author: arefk
"""

import os
import numpy as np

# Function to combine affine matrices
def combine_affine_matrices(affine_matrix_func_path, affine_matrix_dwi_path):
    affine_func = np.loadtxt(affine_matrix_func_path)
    affine_dwi = np.loadtxt(affine_matrix_dwi_path)

    translation_scaling = np.eye(4)
    translation_scaling[:, 3] = affine_func[:, 3]

    rotation_shearing = affine_dwi.copy()
    rotation_shearing[:, 3] = 0

    affine_combined = np.dot(rotation_shearing, translation_scaling)

    return affine_combined

# Main script
initial_path = input("Enter the initial path: ")

for root, dirs, files in os.walk(initial_path):
    if 'func' in dirs:
        func_path = os.path.join(root, 'func')
        for file in files:
            if file.endswith("AffineTrafo.txt"):
                affine_func_path = os.path.join(func_path, file)
                parent_dir = os.path.dirname(os.path.dirname(affine_func_path))
                dwi_path = os.path.join(parent_dir, 'DVI', 'dwi')
                if os.path.exists(dwi_path):
                    for dwi_file in os.listdir(dwi_path):
                        if dwi_file == "AffineTrafo.txt":
                            affine_dwi_path = os.path.join(dwi_path, dwi_file)
                            affine_combined = combine_affine_matrices(affine_func_path, affine_dwi_path)
                            deprecated_path = os.path.join(func_path, "AffineMatrix_deprecated.txt")
                            if os.path.exists(deprecated_path):
                                os.remove(deprecated_path)
                            os.rename(affine_func_path, deprecated_path)
                            np.savetxt(affine_func_path, affine_combined, fmt='%f', delimiter=' ')
                            print(f"Combined and saved affine matrices for {file}")
                            break



!!Not tested yet!! Just the base frame of what I want to do!