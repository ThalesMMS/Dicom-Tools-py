"""Shared utilities for DICOM Tools.

This module centralizes reusable helpers so both the CLI and web layers
can rely on the same implementations.
"""

from .datasets import ensure_pixel_data, load_dataset, save_dataset
from .factories import build_synthetic_series
from .images import calculate_statistics, frame_to_png_bytes, get_frame, window_frame
from .metadata import summarize_metadata
from .network import VerificationServer, send_c_echo

__all__ = [
    "ensure_pixel_data",
    "load_dataset",
    "save_dataset",
    "build_synthetic_series",
    "calculate_statistics",
    "frame_to_png_bytes",
    "get_frame",
    "window_frame",
    "summarize_metadata",
    "VerificationServer",
    "send_c_echo",
]
