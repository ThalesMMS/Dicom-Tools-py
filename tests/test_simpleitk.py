import pytest


sitk = pytest.importorskip("SimpleITK")


def test_simpleitk_filter_preserves_shape(synthetic_series):
    paths, _ = synthetic_series
    image = sitk.ReadImage([str(p) for p in paths])
    smoothed = sitk.SmoothingRecursiveGaussian(image, sigma=1.5)

    array = sitk.GetArrayFromImage(smoothed)
    assert array.shape[0] == len(paths)
    assert array.shape[-2:] == (32, 32)
    assert array.dtype.kind in {"i", "u", "f"}
