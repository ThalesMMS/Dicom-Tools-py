import pytest
import numpy as np

dicom_numpy = pytest.importorskip("dicom_numpy")


def test_dicom_numpy_combine_slices(synthetic_datasets):
    voxel_array, affine = dicom_numpy.combine_slices(synthetic_datasets)

    assert sorted(voxel_array.shape) == sorted((len(synthetic_datasets), 32, 32))
    assert affine.shape == (4, 4)
    assert np.allclose(affine[2, 2], 1.0)
