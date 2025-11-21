import dicom_numpy
import pydicom
import os
import sys
import numpy as np

def test_dicom_numpy_combine():
    input_dir = 'input/dcm_series'
    
    # Collect datasets
    datasets = []
    if os.path.exists(input_dir):
        print(f"Reading files from {input_dir}...")
        for fname in os.listdir(input_dir):
            if fname.endswith('.dcm'):
                try:
                    ds = pydicom.dcmread(os.path.join(input_dir, fname))
                    datasets.append(ds)
                except Exception as e:
                    print(f"Skipping {fname}: {e}")
    
    if not datasets:
        # Fallback to the dummy file if created
        dummy_path = 'input/dummy.dcm'
        if os.path.exists(dummy_path):
            print("Using dummy file...")
            datasets.append(pydicom.dcmread(dummy_path))
        else:
            print("No DICOM datasets found.")
            sys.exit(1)

    print(f"Found {len(datasets)} datasets.")

    try:
        voxel_array, affine = dicom_numpy.combine_slices(datasets)
        print(f"Voxel Array Shape: {voxel_array.shape}")
        print(f"Voxel Array Dtype: {voxel_array.dtype}")
        print("Affine Matrix:")
        print(affine)
        print("SUCCESS: combine_slices worked.")
    except Exception as e:
        print(f"FAILURE: combine_slices failed: {e}")
        # dicom-numpy is strict about ImageOrientationPatient and PixelSpacing.
        # If dcm_series has inconsistent spacing or orientation, it will fail.
        # The dummy file might fail because it lacks some tags.
        sys.exit(1)

if __name__ == "__main__":
    test_dicom_numpy_combine()
