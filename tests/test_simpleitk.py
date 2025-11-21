import SimpleITK as sitk
import os
import sys

def test_simpleitk_filter():
    input_file = 'input/dcm_series/IM-0001-0001.dcm'
    output_file = 'output/simpleitk_test.nii'

    if not os.path.exists(input_file):
        if os.path.exists('input/dummy.dcm'):
            input_file = 'input/dummy.dcm'
        else:
            print("Input file not found.")
            sys.exit(1)

    # 1. Read Image
    print(f"Reading {input_file}...")
    image = sitk.ReadImage(input_file)

    # 2. Print info
    print(f"Size: {image.GetSize()}")
    print(f"Spacing: {image.GetSpacing()}")
    print(f"Origin: {image.GetOrigin()}")
    print(f"Direction: {image.GetDirection()}")

    # Extract 2D slice if 3D (to avoid Z-axis filter issues on single slice)
    if image.GetDimension() == 3 and image.GetSize()[2] == 1:
        print("Extracting 2D slice...")
        image = image[:, :, 0]

    # 3. Apply filter
    print("Applying SmoothingRecursiveGaussianImageFilter...")
    gaussian = sitk.SmoothingRecursiveGaussianImageFilter()
    gaussian.SetSigma(2.0)
    smooth_image = gaussian.Execute(image)

    # 4. Save result
    print(f"Saving to {output_file}...")
    sitk.WriteImage(smooth_image, output_file)
    print("SUCCESS: SimpleITK test completed.")

if __name__ == "__main__":
    test_simpleitk_filter()
