from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp
import os
import tempfile
import uuid

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    try:
        # Create temporary directory for download
        temp_dir = tempfile.mkdtemp()
        filename = f"{uuid.uuid4()}.mp4"
        filepath = os.path.join(temp_dir, filename)
        
        ydl_opts = {
            'format': 'best',
            'outtmpl': filepath,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'video')
        
        # Rename file to actual title
        final_filename = f"{title}.mp4"
        final_filepath = os.path.join(temp_dir, final_filename)
        os.rename(filepath, final_filepath)
        
        return send_file(final_filepath, as_attachment=True, download_name=final_filename)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
