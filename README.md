# DICOM Library Testing Grounds

This repository is dedicated to testing and experimenting with various Python DICOM libraries. The goal is to provide simple, isolated test scripts to demonstrate and verify functionalities of:

- **pydicom**: Reading, writing, and modifying DICOM tags.
- **pynetdicom**: Networking (SCU/SCP) capabilities.
- **gdcm-python**: Decompression and advanced DICOM handling.
- **SimpleITK**: Image IO and basic processing.
- **dicom-numpy**: Converting DICOM datasets to NumPy arrays.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: You may need to install `gdcm` separately if not available on PyPI for your platform).*

2.  **Prepare Input Data**:
    Place your test `.dcm` files in the `input/` directory.
    ```bash
    mkdir input
    # Copy your .dcm files here
    ```

## Structure

- `input/`: Directory for test DICOM files (ignored by git).
- `tests/`: (Planned) Directory containing test scripts for each library.

## Usage



Refer to individual scripts (to be implemented) for specific library tests.



## Included DICOM Tools

This repository also houses a comprehensive suite of CLI utilities (located in `DICOM_reencoder/`) for working with DICOM files. These tools are preserved for legacy support and testing verification.



### Available Scripts

*   **Inspection**: `extract_metadata.py`, `dicom_info.py`, `comparar_dicom.py`

*   **Conversion**: `reencode_dicom.py`, `decompress_dicom.py`, `convert_to_image.py`

*   **Privacy/Validation**: `anonymize_dicom.py`, `validate_dicom.py`, `pixel_stats.py`

*   **Management**: `modify_tags.py`, `organize_dicom.py`, `search_dicom.py`, `split_multiframe.py`, `batch_process.py`

*   **Networking**: `dicom_query.py` (C-FIND), `dicom_retrieve.py` (C-MOVE/C-GET)

*   **Web**: `web_interface.py` (Flask UI)
