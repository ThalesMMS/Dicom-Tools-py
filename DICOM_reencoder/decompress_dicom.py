import sys
import pydicom
from pydicom.uid import ExplicitVRLittleEndian

def main():
    input_file = "1.dcm"
    output_file = "1_decompressed.dcm"
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]

    try:
        # Force reading compressed images
        dataset = pydicom.dcmread(input_file, force=True)
    except FileNotFoundError:
        print(f"Error: File {input_file} not found.")
        sys.exit(1)

    # Ensure the image is decompressed
    if dataset.file_meta.TransferSyntaxUID.is_compressed:
        try:
            dataset.decompress()
        except Exception as e:
            print(f"Error decompressing: {e}")
            sys.exit(1)

    # Update metadata to an uncompressed syntax
    dataset.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

    # Save a new version readable by OsiriX
    dataset.save_as(output_file)
    print(f"Decompressed image saved in: {output_file}")

if __name__ == "__main__":
    main()