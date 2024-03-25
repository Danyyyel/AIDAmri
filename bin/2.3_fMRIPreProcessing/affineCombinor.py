import os
import glob
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
initial_path = r"E:\CRC_data\proc_test"
search_path = os.path.join(initial_path, "*", "*", "func", "*MatrixAff.txt")
afine_trafos = glob.glob(search_path)

for affine_func_path in afine_trafos:
    parent_dir = os.path.dirname(os.path.dirname(affine_func_path))
    dwi_path = os.path.join(parent_dir, 'dwi')
    
    if os.path.exists(dwi_path):
        affine_dwi_path = glob.glob(os.path.join(dwi_path, "*MatrixAff.txt"))[0]
        
        if os.path.exists(affine_dwi_path):
            affine_combined = combine_affine_matrices(affine_func_path, affine_dwi_path)
            
            deprecated_path = os.path.join(os.path.dirname(affine_func_path), "AffineMatrix_deprecated.txt")
            if os.path.exists(deprecated_path):
                os.remove(deprecated_path)
            
            os.rename(affine_func_path, deprecated_path)
            np.savetxt(affine_func_path, affine_combined, fmt='%f', delimiter=' ')
            print(f"Combined and saved affine matrices for {os.path.basename(affine_func_path)}")
        else:
            print(f"No DWI AffineTrafo found for {os.path.basename(affine_func_path)}")
    else:
        print(f"No DWI directory found for {os.path.basename(affine_func_path)}")
