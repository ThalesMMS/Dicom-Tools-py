import pydicom
from pydicom.uid import ExplicitVRLittleEndian

input_file = "1.dcm"
output_file = "1_decompressed.dcm"

# Force reading compressed images
dataset = pydicom.dcmread(input_file, force=True)

# Ensure the image is decompressed
if dataset.file_meta.TransferSyntaxUID.is_compressed:
    dataset.decompress()

# Update metadata to an uncompressed syntax
dataset.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

# Save a new version readable by OsiriX
dataset.save_as(output_file)
print(f"Decompressed image saved in: {output_file}")
