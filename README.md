# DICOM Tools

Python utilities for inspecting, decompressing, and re-encoding DICOM studies. The repository currently ships three standalone scripts backed by the [`pydicom`](https://pydicom.github.io/) toolkit:

- `reencode_dicom.py` rewrites a DICOM file with the explicit little-endian transfer syntax.
- `decompress_dicom.py` forces decompression of a DICOM file and saves an uncompressed copy that is compatible with legacy viewers such as OsiriX.
- `comparar_dicom.py` compares metadata between two DICOM files and highlights any differences.

## Repository Layout

```
DICOM_reencoder/
├── comparar_dicom.py
├── decompress_dicom.py
└── reencode_dicom.py
```

Each script expects to be run from a directory containing the target `.dcm` files. All scripts read hard-coded filenames (`1.dcm`, `2.dcm`, and so on); adjust these variables or refactor the scripts if you need to work with different names.

## Requirements

- Python 3.9 or newer
- `pydicom`

Install dependencies with:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -U pip
pip install pydicom
```

## Usage

Run any script from the project root (or the folder containing the `.dcm` files):

```bash
python DICOM_reencoder/reencode_dicom.py
```

### Re-encode a DICOM file

`reencode_dicom.py` reads `1.dcm`, rewrites it using the Explicit VR Little Endian transfer syntax, and outputs `1_reencoded.dcm`.

### Decompress a DICOM file

`decompress_dicom.py` reads `1.dcm`, decompresses the pixel data if needed, and writes `1_decompressed.dcm` with an explicit little-endian transfer syntax.

### Compare metadata between two files

`comparar_dicom.py` reads `1.dcm` and `2.dcm` and prints a side-by-side comparison of key metadata attributes, flagging differences inline.

## Next Steps

- Generalize the scripts to accept command-line arguments (for example using `argparse`).
- Add automated tests with sample DICOM files to validate expected behavior.
- Package the utilities as a module or CLI entry points for easier distribution.

## License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE) for details.
