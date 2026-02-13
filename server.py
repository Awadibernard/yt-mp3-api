from flask import Flask, request, Response, jsonify
import subprocess
import tempfile
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "API yt-dlp OK"

@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()

    if not data or "videoId" not in data:
        return jsonify({"error": "videoId manquant"}), 400

    video_id = data["videoId"]

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "%(title)s.%(ext)s")

        command = [
            "yt-dlp",
            "-x",
            "--audio-format", "mp3",
            "-o", output_path,
            f"https://www.youtube.com/watch?v={video_id}"
        ]

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            return jsonify({
                "error": "yt-dlp a échoué",
                "details": result.stderr
            }), 500

        # Récupérer le fichier généré
        files = os.listdir(tmpdir)
        if not files:
            return jsonify({"error": "Fichier audio non généré"}), 500

        file_path = os.path.join(tmpdir, files[0])

        with open(file_path, "rb") as f:
            audio_data = f.read()

    return Response(
        audio_data,
        mimetype="audio/mpeg",
        headers={
            "Content-Disposition": f'attachment; filename="{video_id}.mp3"'
        }
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
