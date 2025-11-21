import pytest


gdcm = pytest.importorskip("gdcm")


def test_gdcm_reads_synthetic_dicom(synthetic_dicom_path):
    reader = gdcm.ImageReader()
    reader.SetFileName(str(synthetic_dicom_path))
    assert reader.Read()

    image = reader.GetImage()
    dims = image.GetDimensions()
    assert dims[0] == 32
    assert dims[1] == 32
    assert image.GetBufferLength() > 0
