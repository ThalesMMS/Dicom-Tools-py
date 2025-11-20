#!/usr/bin/env python3

import pydicom
from pydicom.uid import ExplicitVRLittleEndian

input_file = "1.dcm"
output_file = "1_reencoded.dcm"

dataset = pydicom.dcmread(input_file, force=True)

# Define new Transfer Syntax
dataset.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

# Save as new file
dataset.save_as(output_file)
print(f"File rewritten with TransferSyntaxUID={ExplicitVRLittleEndian} in '{output_file}'")
