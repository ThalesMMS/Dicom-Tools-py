from DICOM_reencoder.core import calculate_statistics, load_dataset, save_dataset, summarize_metadata


def test_pydicom_roundtrip(synthetic_dicom_path, tmp_path):
    dataset = load_dataset(synthetic_dicom_path)
    dataset.PatientName = "Unit^Test"

    output = save_dataset(dataset, tmp_path / "roundtrip.dcm")
    reloaded = load_dataset(output)

    assert str(reloaded.PatientName) == "Unit^Test"

    summary = summarize_metadata(reloaded)
    assert summary["patient"]["id"] == "TEST-123"

    stats = calculate_statistics(reloaded.pixel_array)
    assert stats["total_pixels"] == reloaded.Rows * reloaded.Columns
    assert stats["min"] >= 0
