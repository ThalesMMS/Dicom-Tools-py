#!/usr/bin/env python3
import sys
import pydicom
from pydicom.uid import ExplicitVRLittleEndian

def main():
    input_file = "1.dcm"
    output_file = "1_reencoded.dcm"
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]

    print(f"Reading {input_file}...")
    try:
        dataset = pydicom.dcmread(input_file, force=True)
    except FileNotFoundError:
        print(f"Error: File {input_file} not found.")
        sys.exit(1)

    # Define new Transfer Syntax
    dataset.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

    # Save as new file
    dataset.save_as(output_file)
    print(f"File rewritten with TransferSyntaxUID={ExplicitVRLittleEndian} in '{output_file}'")

if __name__ == "__main__":
    main()