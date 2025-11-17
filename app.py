from flask import Flask, render_template, jsonify, request
import subprocess

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add_faces")
def run_script1():
    filename = request.args.get("filename")
    cmd = ["python3", "take_pic.py"]
    if filename:
        cmd.append(filename)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return jsonify({"output": result.stdout, "error": result.stderr})

@app.route("/find_faces")
def run_script2():
    # Run script2.py
    result = subprocess.run(["python3", "check_faces.py"], capture_output=True, text=True)
    return jsonify({"output": result.stdout, "error": result.stderr})

if __name__ == "__main__":
    app.run(debug=True)