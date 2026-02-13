from flask import Flask, request, Response
import subprocess, os, tempfile

app = Flask(__name__)

@app.route("/download", methods=["POST"])
def download():
    data = request.json
    video_id = data.get("videoId")

    if not video_id:
        return {"error": "videoId required"}, 400

    with tempfile.TemporaryDirectory() as tmpdir:
        output = os.path.join(tmpdir, "audio.mp3")

        result = subprocess.run([
            "yt-dlp",
            "-x",
            "--audio-format", "mp3",
            "-o", output,
            f"https://youtube.com/watch?v={video_id}"
        ], capture_output=True, text=True)

        if result.returncode != 0:
            return {"error": result.stderr}, 500

        with open(output, "rb") as f:
            audio = f.read()

    return Response(
        audio,
        mimetype="audio/mpeg",
        headers={
            "Content-Disposition": f'attachment; filename=\"{video_id}.mp3\"'
        }
)
