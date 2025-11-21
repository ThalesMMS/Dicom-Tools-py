import os
import sys
import pydicom
from pydicom.dataset import Dataset, FileDataset
from pydicom.uid import ExplicitVRLittleEndian
import datetime

def test_pydicom_basic():
    input_file = 'input/dcm_series/IM-0001-0001.dcm'
    output_file = 'output/pydicom_test.dcm'

    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Input file not found: {input_file}")
        # Try to find any .dcm file in input/
        found = False
        for root, dirs, files in os.walk('input'):
            for file in files:
                if file.endswith('.dcm'):
                    input_file = os.path.join(root, file)
                    print(f"Using alternative file: {input_file}")
                    found = True
                    break
            if found:
                break
        
        if not found:
            print("No DICOM files found in input/. Generating a dummy one.")
            # Create a dummy DICOM file
            file_meta = Dataset()
            file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2'
            file_meta.MediaStorageSOPInstanceUID = "1.2.3"
            file_meta.ImplementationClassUID = "1.2.3.4"
            file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

            ds = FileDataset(input_file, {}, file_meta=file_meta, preamble=b"\0" * 128)
            ds.PatientName = "Test^Patient"
            ds.PatientID = "123456"
            ds.Modality = "CT"
            ds.is_little_endian = True
            ds.is_implicit_VR = False
            
            # Save it so we can "load" it
            input_file = 'input/dummy.dcm'
            if not os.path.exists('input'):
                os.makedirs('input')
            ds.save_as(input_file)
            print(f"Created dummy file: {input_file}")

    # 1. Load a DICOM file
    print(f"Loading {input_file}...")
    ds = pydicom.dcmread(input_file)

    # 2. Print specific tags
    print("Original PatientName:", ds.get("PatientName", "N/A"))
    print("Original Modality:", ds.get("Modality", "N/A"))

    # 3. Modify a tag
    new_name = "TEST^PATIENT"
    print(f"Modifying PatientName to {new_name}...")
    ds.PatientName = new_name

    # 4. Save the file
    print(f"Saving to {output_file}...")
    ds.save_as(output_file)

    # 5. Reload and verify
    print(f"Reloading {output_file}...")
    ds_new = pydicom.dcmread(output_file)
    print("New PatientName:", ds_new.PatientName)

    if ds_new.PatientName == new_name:
        print("SUCCESS: PatientName was successfully modified.")
    else:
        print("FAILURE: PatientName mismatch.")
        sys.exit(1)

if __name__ == "__main__":
    test_pydicom_basic()
