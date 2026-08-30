from flask import Flask, render_template, request, send_file
import subprocess
import os
import uuid

app = Flask(__name__)

MODEL = os.path.expanduser(
    "~/Desktop/sulei-voice-clone/exports/sulei-epoch150.onnx"
)

OUTPUT_DIR = os.path.expanduser(
    "~/Desktop/sulei-voice-clone/outputs"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])

def generate():
    text = request.form.get("text", "").strip()

    if not text:
        return { "error": "Please enter some text."}, 400

    filename = f"{uuid.uuid4()}.wav"
    output_file = os.path.join(OUTPUT_DIR, filename)

    try:
        subprocess.run(
            [
                "python",
                "-m",
                "piper",
                "--model",
                MODEL,
                "--output_file",
                output_file,
            ],
            input = text,
            text = True,
            check = True,
        )

        return send_file(
            output_file,
            mimetype="audio_wav",
            as_attachment=False,
        )
    except subprocess.CalledProcessError as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(debug=True)