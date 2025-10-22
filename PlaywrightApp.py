import uuid
import base64
from threading import Thread
from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

jobs = {}

def run_playwright_job(job_id, url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=30000)  # 30s navigation timeout
            # Example: take screenshot
            image_bytes = page.screenshot(full_page=True)
            browser.close()

        # Store result as base64 to keep JSON-friendly
        jobs[job_id]["status"] = "done"
        jobs[job_id]["result"] = base64.b64encode(image_bytes).decode("ascii")
    except Exception as e:
        jobs[job_id]["status"] = "error"
        jobs[job_id]["error"] = str(e)

@app.route("/run", methods=["POST"])
def start_job():
    data = request.get_json(force=True)
    url = data.get("url")
    if not url:
        return jsonify({"error": "missing url"}), 400

    # simple auth check (optional) - set SECRET_TOKEN as env var on Render
    secret = app.config.get("SECRET_TOKEN")
    if secret:
        token = request.headers.get("Authorization", "")
        if token != f"Bearer {secret}":
            return jsonify({"error": "unauthorized"}), 401

    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "started"}
    Thread(target=run_playwright_job, args=(job_id, url), daemon=True).start()
    return jsonify({"job_id": job_id, "status": "started"}), 202

@app.route("/status/<job_id>", methods=["GET"])
def job_status(job_id):
    j = jobs.get(job_id)
    if not j:
        return jsonify({"error": "not found"}), 404
    return jsonify(j)

if __name__ == "__main__":
    # Render typically sets PORT env var; fallback to 10000
    import os
    port = int(os.environ.get("PORT", 10000))
    # Optionally load secret token from environment for simple protection
    app.config["SECRET_TOKEN"] = os.environ.get("SECRET_TOKEN")
    app.run(host="0.0.0.0", port=port)
