from http.server import BaseHTTPRequestHandler
from gtts import gTTS
import json
import tempfile
import os

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = json.loads(body.decode('utf-8'))

        text = data.get("text", "Assalamualaikum")
        lang = data.get("lang", "ur")

        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        temp.close()

        gTTS(text=text, lang=lang).save(temp.name)

        with open(temp.name, "rb") as f:
            audio = f.read()

        os.remove(temp.name)

        self.send_response(200)
        self.send_header("Content-Type", "audio/mpeg")
        self.end_headers()
        self.wfile.write(audio)