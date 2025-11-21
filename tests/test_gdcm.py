import sys
import gdcm
import os

def test_gdcm_read():
    input_file = 'input/dcm_series/IM-0001-0001.dcm'
    
    # Use dummy if original doesn't exist (created in previous test)
    if not os.path.exists(input_file):
        if os.path.exists('input/dummy.dcm'):
            input_file = 'input/dummy.dcm'
        else:
            print("No input file found.")
            sys.exit(1)

    print(f"Reading {input_file} using GDCM...")
    
    reader = gdcm.ImageReader()
    reader.SetFileName(input_file)
    if not reader.Read():
        print("FAILURE: GDCM could not read the file.")
        sys.exit(1)

    image = reader.GetImage()
    dims = image.GetDimensions()
    print(f"Dimensions: {dims}")
    
    pixel_format = image.GetPixelFormat()
    print(f"Pixel Format: {pixel_format.GetScalarTypeAsString()}")
    
    buffer_length = image.GetBufferLength()
    print(f"Buffer Length: {buffer_length}")
    
    # Try to get the buffer
    try:
        # Attempt 1: No arguments (maybe returns bytes)
        buffer = image.GetBuffer()
        print(f"Successfully retrieved pixel buffer (type: {type(buffer)}).")
    except TypeError:
        try:
            # Attempt 2: Pass buffer (maybe swig issue resolved)
            buffer = bytearray(buffer_length)
            image.GetBuffer(buffer)
            print("Successfully retrieved pixel buffer into bytearray.")
        except Exception as e:
            print(f"Failed to get buffer: {e}")

    print("SUCCESS: GDCM read and decoded the image.")

if __name__ == "__main__":
    test_gdcm_read()
