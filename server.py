from flask import Flask, request, Response, jsonify
import subprocess
import os
import tempfile

app = Flask(__name__)

@app.route("/download", methods=["POST"])
def download():
    data = request.json
    video_id = data.get("videoId")

    if not video_id:
        return jsonify({"error": "videoId requis"}), 400

    with tempfile.TemporaryDirectory() as tmpdir:
        output = os.path.join(tmpdir, "audio.mp3")

        command = [
            "yt-dlp",
            "-x",
            "--audio-format", "mp3",
            "--cookies", "/app/cookies.txt",
            "-o", output,
            f"https://www.youtube.com/watch?v={video_id}"
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return jsonify({
                "error": "yt-dlp a échoué",
                "details": result.stderr
            }), 500

        with open(output, "rb") as f:
            audio = f.read()

    return Response(
        audio,
        mimetype="audio/mpeg",
        headers={
            "Content-Disposition": f'attachment; filename="{video_id}.mp3"'
        }
    )

@app.route("/")
def health():
    return "API yt-dlp OK", 200
