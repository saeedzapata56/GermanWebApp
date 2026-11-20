from flask import Flask, render_template, request, jsonify
from gtts import gTTS
import os
import uuid

app = Flask(__name__)
AUDIO_FOLDER = os.path.join('static', 'audio')
os.makedirs(AUDIO_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        if not text:
            return jsonify({'success': False, 'error': 'No text provided'})

        filename = f"voice_{uuid.uuid4().hex}.mp3"
        filepath = os.path.join(AUDIO_FOLDER, filename)
        
        tts = gTTS(text=text, lang='de', slow=False)
        tts.save(filepath)

        audio_url = f"/static/audio/{filename}"
        return jsonify({'success': True, 'audio_url': audio_url})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)