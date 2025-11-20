#!/usr/bin/env python3
"""
Web interface for DICOM Tools.
This provides a Flask-based web interface for DICOM file operations
including viewing, conversion, anonymization, and validation.
"""

import sys
import os
import argparse
import tempfile
import base64
from io import BytesIO
from pathlib import Path

from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

import pydicom
from pydicom.uid import ExplicitVRLittleEndian
import numpy as np

# Import our modules
try:
    from . import (
        extract_metadata,
        anonymize_dicom,
        validate_dicom,
        pixel_stats,
        convert_to_image,
    )
except ImportError:
    # Fallback for direct execution
    pass

app = Flask(__name__,
            template_folder='web_templates',
            static_folder='web_static')
CORS(app)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp(prefix='dicom_web_')
app.config['ALLOWED_EXTENSIONS'] = {'dcm', 'dicom', 'DCM', 'DICOM'}

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload DICOM file."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Try to read as DICOM
        try:
            ds = pydicom.dcmread(filepath, force=True)

            # Extract basic info
            info = {
                'filename': filename,
                'patient_name': str(ds.get('PatientName', 'N/A')),
                'patient_id': str(ds.get('PatientID', 'N/A')),
                'study_date': str(ds.get('StudyDate', 'N/A')),
                'modality': str(ds.get('Modality', 'N/A')),
                'study_description': str(ds.get('StudyDescription', 'N/A')),
                'has_pixel_data': 'PixelData' in ds,
            }

            return jsonify({'success': True, 'info': info, 'filename': filename})

        except Exception as e:
            os.remove(filepath)
            return jsonify({'error': f'Not a valid DICOM file: {str(e)}'}), 400


@app.route('/api/metadata/<filename>')
def get_metadata(filename):
    """Get detailed metadata for a DICOM file."""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))

    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404

    try:
        ds = pydicom.dcmread(filepath, force=True)

        metadata = {
            'patient': {
                'name': str(ds.get('PatientName', 'N/A')),
                'id': str(ds.get('PatientID', 'N/A')),
                'birth_date': str(ds.get('PatientBirthDate', 'N/A')),
                'sex': str(ds.get('PatientSex', 'N/A')),
                'age': str(ds.get('PatientAge', 'N/A')),
            },
            'study': {
                'description': str(ds.get('StudyDescription', 'N/A')),
                'date': str(ds.get('StudyDate', 'N/A')),
                'time': str(ds.get('StudyTime', 'N/A')),
                'id': str(ds.get('StudyID', 'N/A')),
                'instance_uid': str(ds.get('StudyInstanceUID', 'N/A')),
            },
            'series': {
                'description': str(ds.get('SeriesDescription', 'N/A')),
                'number': str(ds.get('SeriesNumber', 'N/A')),
                'modality': str(ds.get('Modality', 'N/A')),
                'instance_uid': str(ds.get('SeriesInstanceUID', 'N/A')),
            },
            'image': {
                'instance_number': str(ds.get('InstanceNumber', 'N/A')),
                'rows': str(ds.get('Rows', 'N/A')),
                'columns': str(ds.get('Columns', 'N/A')),
                'bits_allocated': str(ds.get('BitsAllocated', 'N/A')),
                'photometric_interpretation': str(ds.get('PhotometricInterpretation', 'N/A')),
            }
        }

        return jsonify(metadata)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/image/<filename>')
def get_image(filename):
    """Get DICOM image as PNG."""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))

    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404

    try:
        from PIL import Image

        ds = pydicom.dcmread(filepath, force=True)

        if 'PixelData' not in ds:
            return jsonify({'error': 'No pixel data in file'}), 400

        # Get pixel array
        pixel_array = ds.pixel_array

        # Handle multi-frame (use first frame)
        if len(pixel_array.shape) > 2:
            pixel_array = pixel_array[0]

        # Apply windowing
        wc = ds.get('WindowCenter', None)
        ww = ds.get('WindowWidth', None)

        if wc is not None and ww is not None:
            if isinstance(wc, pydicom.multival.MultiValue):
                wc = int(wc[0])
                ww = int(ww[0])
            else:
                wc = int(wc)
                ww = int(ww)
        else:
            # Auto window
            wc = int(np.median(pixel_array))
            ww = int(np.percentile(pixel_array, 95) - np.percentile(pixel_array, 5))

        # Apply window
        img_min = wc - ww // 2
        img_max = wc + ww // 2
        windowed = np.clip(pixel_array, img_min, img_max)
        windowed = ((windowed - img_min) / (img_max - img_min) * 255.0).astype(np.uint8)

        # Handle MONOCHROME1
        if ds.get('PhotometricInterpretation') == 'MONOCHROME1':
            windowed = 255 - windowed

        # Convert to image
        img = Image.fromarray(windowed)

        # Save to bytes
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)

        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/validate/<filename>')
def validate_file(filename):
    """Validate a DICOM file."""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))

    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404

    try:
        from .validate_dicom import DicomValidator

        validator = DicomValidator()
        is_valid = validator.validate_file(filepath)

        return jsonify({
            'valid': is_valid,
            'errors': validator.errors,
            'warnings': validator.warnings,
            'info': validator.info
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/anonymize/<filename>', methods=['POST'])
def anonymize_file(filename):
    """Anonymize a DICOM file."""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))

    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404

    try:
        # Create output filename
        output_filename = f"anon_{filename}"
        output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

        # Anonymize
        from .anonymize_dicom import anonymize_dicom
        anonymize_dicom(filepath, output_filepath)

        return jsonify({
            'success': True,
            'filename': output_filename
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/download/<filename>')
def download_file(filename):
    """Download a DICOM file."""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))

    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404

    return send_file(filepath, as_attachment=True, download_name=filename)


@app.route('/api/stats/<filename>')
def get_pixel_stats(filename):
    """Get pixel statistics for a DICOM file."""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))

    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404

    try:
        ds = pydicom.dcmread(filepath, force=True)

        if 'PixelData' not in ds:
            return jsonify({'error': 'No pixel data in file'}), 400

        pixel_array = ds.pixel_array

        # Handle multi-frame
        if len(pixel_array.shape) > 2:
            pixel_array = pixel_array[0]

        from .pixel_stats import calculate_statistics
        stats = calculate_statistics(pixel_array)

        return jsonify(stats)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def create_default_templates():
    """Create default HTML templates if they don't exist."""
    template_dir = os.path.join(os.path.dirname(__file__), 'web_templates')
    os.makedirs(template_dir, exist_ok=True)

    index_html = os.path.join(template_dir, 'index.html')

    if not os.path.exists(index_html):
        with open(index_html, 'w') as f:
            f.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DICOM Tools Web Interface</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif; background: #f5f5f5; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        header { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 20px; }
        h1 { color: #333; font-size: 2em; margin-bottom: 10px; }
        h1::before { content: "🏥 "; }
        .subtitle { color: #666; font-size: 1.1em; }
        .main-content { display: grid; grid-template-columns: 1fr 2fr; gap: 20px; }
        .panel { background: white; padding: 25px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .upload-area { border: 3px dashed #ddd; border-radius: 10px; padding: 40px; text-align: center; cursor: pointer; transition: all 0.3s; }
        .upload-area:hover { border-color: #4CAF50; background: #f9f9f9; }
        .upload-area.dragover { border-color: #4CAF50; background: #e8f5e9; }
        .btn { background: #4CAF50; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; font-size: 1em; margin: 5px; transition: all 0.3s; }
        .btn:hover { background: #45a049; transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
        .btn:disabled { background: #ccc; cursor: not-allowed; transform: none; }
        .btn-secondary { background: #2196F3; }
        .btn-secondary:hover { background: #0b7dda; }
        .btn-danger { background: #f44336; }
        .btn-danger:hover { background: #da190b; }
        #imageView { max-width: 100%; border-radius: 5px; margin-top: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .metadata { margin-top: 15px; }
        .metadata-section { margin-bottom: 15px; }
        .metadata-section h3 { color: #4CAF50; margin-bottom: 10px; font-size: 1.2em; }
        .metadata-item { display: flex; padding: 8px 0; border-bottom: 1px solid #eee; }
        .metadata-item:last-child { border-bottom: none; }
        .metadata-label { font-weight: bold; min-width: 150px; color: #666; }
        .metadata-value { color: #333; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-top: 15px; }
        .stat-card { background: #f9f9f9; padding: 15px; border-radius: 5px; text-align: center; }
        .stat-value { font-size: 1.5em; font-weight: bold; color: #4CAF50; }
        .stat-label { color: #666; margin-top: 5px; font-size: 0.9em; }
        .alert { padding: 15px; border-radius: 5px; margin: 15px 0; }
        .alert-success { background: #d4edda; border: 1px solid #c3e6cb; color: #155724; }
        .alert-error { background: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; }
        .alert-warning { background: #fff3cd; border: 1px solid #ffeaa7; color: #856404; }
        .loading { display: none; text-align: center; padding: 20px; }
        .loading.active { display: block; }
        .spinner { border: 4px solid #f3f3f3; border-top: 4px solid #4CAF50; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 0 auto; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        footer { text-align: center; margin-top: 30px; padding: 20px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>DICOM Tools Web Interface</h1>
            <p class="subtitle">Upload, view, and process DICOM medical images</p>
        </header>

        <div class="main-content">
            <div class="panel">
                <h2>📤 Upload DICOM File</h2>
                <div class="upload-area" id="uploadArea">
                    <p style="font-size: 3em; margin-bottom: 10px;">📁</p>
                    <p>Drag and drop a DICOM file here</p>
                    <p style="color: #999; margin: 10px 0;">or</p>
                    <input type="file" id="fileInput" accept=".dcm,.dicom" style="display: none;">
                    <button class="btn" onclick="document.getElementById('fileInput').click()">Browse Files</button>
                </div>

                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <p style="margin-top: 15px;">Processing...</p>
                </div>

                <div id="fileInfo" style="margin-top: 20px; display: none;">
                    <h3>📋 File Information</h3>
                    <div class="metadata-item">
                        <span class="metadata-label">Patient:</span>
                        <span class="metadata-value" id="infoPatient"></span>
                    </div>
                    <div class="metadata-item">
                        <span class="metadata-label">Modality:</span>
                        <span class="metadata-value" id="infoModality"></span>
                    </div>
                    <div class="metadata-item">
                        <span class="metadata-label">Study Date:</span>
                        <span class="metadata-value" id="infoStudyDate"></span>
                    </div>

                    <div style="margin-top: 20px;">
                        <button class="btn" onclick="showMetadata()">📊 View Metadata</button>
                        <button class="btn btn-secondary" onclick="showStats()">📈 Pixel Stats</button>
                        <button class="btn btn-secondary" onclick="anonymize()">🔒 Anonymize</button>
                        <button class="btn btn-danger" onclick="validate()">✓ Validate</button>
                    </div>
                </div>
            </div>

            <div class="panel">
                <h2>🖼️ Image Viewer</h2>
                <div id="viewerContent">
                    <p style="text-align: center; color: #999; padding: 60px 20px;">Upload a DICOM file to view</p>
                </div>
            </div>
        </div>
    </div>

    <footer>
        <p>DICOM Tools v1.0.0 | Built with Flask & pydicom</p>
    </footer>

    <script>
        let currentFilename = null;

        // File upload handling
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');

        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            const file = e.dataTransfer.files[0];
            if (file) uploadFile(file);
        });

        fileInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) uploadFile(file);
        });

        async function uploadFile(file) {
            const formData = new FormData();
            formData.append('file', file);

            document.getElementById('loading').classList.add('active');
            document.getElementById('fileInfo').style.display = 'none';
            document.getElementById('viewerContent').innerHTML = '<p style="text-align: center; color: #999; padding: 60px 20px;">Loading...</p>';

            try {
                const response = await fetch('/api/upload', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                if (data.success) {
                    currentFilename = data.filename;
                    document.getElementById('infoPatient').textContent = data.info.patient_name;
                    document.getElementById('infoModality').textContent = data.info.modality;
                    document.getElementById('infoStudyDate').textContent = data.info.study_date;
                    document.getElementById('fileInfo').style.display = 'block';

                    if (data.info.has_pixel_data) {
                        document.getElementById('viewerContent').innerHTML =
                            `<img id="imageView" src="/api/image/${data.filename}" alt="DICOM Image">`;
                    } else {
                        document.getElementById('viewerContent').innerHTML =
                            '<p style="text-align: center; color: #999; padding: 60px 20px;">No pixel data in this DICOM file</p>';
                    }
                } else {
                    alert('Error: ' + data.error);
                }
            } catch (error) {
                alert('Upload failed: ' + error.message);
            }

            document.getElementById('loading').classList.remove('active');
        }

        async function showMetadata() {
            if (!currentFilename) return;

            try {
                const response = await fetch(`/api/metadata/${currentFilename}`);
                const data = await response.json();

                let html = '<h3>📋 Complete Metadata</h3><div class="metadata">';

                for (const [category, fields] of Object.entries(data)) {
                    html += `<div class="metadata-section"><h3>${category.toUpperCase()}</h3>`;
                    for (const [key, value] of Object.entries(fields)) {
                        html += `<div class="metadata-item">
                            <span class="metadata-label">${key}:</span>
                            <span class="metadata-value">${value}</span>
                        </div>`;
                    }
                    html += '</div>';
                }

                html += '</div>';
                document.getElementById('viewerContent').innerHTML = html;
            } catch (error) {
                alert('Failed to load metadata: ' + error.message);
            }
        }

        async function showStats() {
            if (!currentFilename) return;

            document.getElementById('viewerContent').innerHTML = '<p style="text-align: center; padding: 60px 20px;">Loading statistics...</p>';

            try {
                const response = await fetch(`/api/stats/${currentFilename}`);
                const data = await response.json();

                let html = '<h3>📊 Pixel Data Statistics</h3>';
                html += '<div class="stats-grid">';

                const stats = [
                    { label: 'Minimum', value: data.min },
                    { label: 'Maximum', value: data.max },
                    { label: 'Mean', value: data.mean.toFixed(2) },
                    { label: 'Median', value: data.median.toFixed(2) },
                    { label: 'Std Dev', value: data.std.toFixed(2) },
                    { label: 'Total Pixels', value: data.total_pixels.toLocaleString() },
                ];

                stats.forEach(stat => {
                    html += `<div class="stat-card">
                        <div class="stat-value">${stat.value}</div>
                        <div class="stat-label">${stat.label}</div>
                    </div>`;
                });

                html += '</div>';
                document.getElementById('viewerContent').innerHTML = html;
            } catch (error) {
                alert('Failed to load statistics: ' + error.message);
            }
        }

        async function anonymize() {
            if (!currentFilename) return;

            if (!confirm('Anonymize this DICOM file? Patient information will be removed.')) return;

            document.getElementById('loading').classList.add('active');

            try {
                const response = await fetch(`/api/anonymize/${currentFilename}`, { method: 'POST' });
                const data = await response.json();

                if (data.success) {
                    alert('File anonymized successfully! Download: ' + data.filename);
                    window.location.href = `/api/download/${data.filename}`;
                } else {
                    alert('Error: ' + data.error);
                }
            } catch (error) {
                alert('Anonymization failed: ' + error.message);
            }

            document.getElementById('loading').classList.remove('active');
        }

        async function validate() {
            if (!currentFilename) return;

            document.getElementById('viewerContent').innerHTML = '<p style="text-align: center; padding: 60px 20px;">Validating...</p>';

            try {
                const response = await fetch(`/api/validate/${currentFilename}`);
                const data = await response.json();

                let html = '<h3>✓ Validation Results</h3>';

                if (data.valid) {
                    html += '<div class="alert alert-success">✓ File is valid!</div>';
                } else {
                    html += '<div class="alert alert-error">✗ Validation failed</div>';
                }

                if (data.errors && data.errors.length > 0) {
                    html += '<div class="metadata-section"><h3>Errors</h3>';
                    data.errors.forEach(err => {
                        html += `<div class="alert alert-error">${err}</div>`;
                    });
                    html += '</div>';
                }

                if (data.warnings && data.warnings.length > 0) {
                    html += '<div class="metadata-section"><h3>Warnings</h3>';
                    data.warnings.forEach(warn => {
                        html += `<div class="alert alert-warning">${warn}</div>`;
                    });
                    html += '</div>';
                }

                document.getElementById('viewerContent').innerHTML = html;
            } catch (error) {
                alert('Validation failed: ' + error.message);
            }
        }
    </script>
</body>
</html>''')


def main():
    """Main entry point for web interface."""
    parser = argparse.ArgumentParser(description='DICOM Tools Web Interface')
    parser.add_argument('-H', '--host', default='127.0.0.1',
                        help='Host to bind to (default: 127.0.0.1)')
    parser.add_argument('-p', '--port', type=int, default=5000,
                        help='Port to bind to (default: 5000)')
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug mode')

    args = parser.parse_args()

    # Create templates
    create_default_templates()

    print(f"\n{'='*80}")
    print("DICOM Tools Web Interface")
    print(f"{'='*80}\n")
    print(f"  Starting server at http://{args.host}:{args.port}")
    print(f"  Press Ctrl+C to stop\n")
    print(f"{'='*80}\n")

    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == '__main__':
    main()
