from http.server import BaseHTTPRequestHandler
from gtts import gTTS
import json, tempfile, os

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("content-length", 0))
        body = self.rfile.read(length)

        data = json.loads(body.decode("utf-8"))
        text = data.get("text", "Assalamualaikum")
        lang = data.get("lang", "ur")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            filename = tmp.name

        gTTS(text=text, lang=lang).save(filename)

        with open(filename, "rb") as f:
            audio = f.read()

        os.remove(filename)

        self.send_response(200)
        self.send_header("Content-Type", "audio/mpeg")
        self.send_header("Content-Disposition", "attachment; filename=voice.mp3")
        self.end_headers()
        self.wfile.write(audio)