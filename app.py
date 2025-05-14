from flask import Flask, request, jsonify, send_from_directory
from yt_dlp import YoutubeDL

app = Flask(__name__)

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

@app.route('/download', methods=['POST'])
def download_video():
    try:
        url = request.json.get('url')
        ydl_opts = {'quiet': True, 'skip_download': True}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                'title': info.get('title'),
                'thumbnail': info.get('thumbnail'),
                'formats': [
                    {'format': f"{f.get('format')} ({f.get('ext')})", 
                     'url': f.get('url')}
                    for f in info.get('formats', []) if f.get('url')
                ]
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename
