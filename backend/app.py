from flask import Flask, send_file, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

FILES_DIR = os.path.join(os.path.dirname(__file__), 'files')

FILE_MAPPINGS = {
    'resume': 'Akhil_Shetty_Resume.pdf',
    'aws': 'AWS_Certificate.pdf',
    'python': 'Python_Certificate.pdf',
}

@app.route('/')
def home():
    return jsonify({
        'status': 'online',
        'message': 'Portfolio Backend API',
        'endpoints': {
            'resume': '/download/resume',
            'certificates': '/download/certificate/<type>',
            'list_files': '/api/files'
        }
    })

@app.route('/download/resume')
def download_resume():
    try:
        file_path = os.path.join(FILES_DIR, FILE_MAPPINGS['resume'])
        return send_file(file_path, as_attachment=True, download_name='Akhil_Shetty_Resume.pdf')
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/download/certificate/<cert_type>')
def download_certificate(cert_type):
    try:
        if cert_type not in FILE_MAPPINGS:
            return jsonify({'error': 'Certificate not found'}), 404
        
        file_path = os.path.join(FILES_DIR, FILE_MAPPINGS[cert_type])
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/api/files')
def list_files():
    available_files = {}
    for key, filename in FILE_MAPPINGS.items():
        file_path = os.path.join(FILES_DIR, filename)
        available_files[key] = {
            'filename': filename,
            'exists': os.path.exists(file_path)
        }
    return jsonify(available_files)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)