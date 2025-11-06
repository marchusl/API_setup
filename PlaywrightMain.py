from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
from threading import Thread
import os, uuid

from tasks.GetScreenshot import take_screenshot
from tasks.ClickButton import click_button

app = Flask(__name__)
jobs = {}

os.makedirs("static/screenshots", exist_ok=True)

@app.route("/")
def home():
    return "✅ Flask + Playwright API is running!"

@app.route("/run", methods=["POST"])
def start_job():
    sent_data = request.get_json(force=True)
    url = sent_data.get("url")
    job_type = sent_data.get("job_type", "NONE")
    params = sent_data.get("params", {})

    if not url:
        return jsonify({"error": "missing url"}), 400

    # Ensure URL includes scheme (http/https)
    if not url.startswith("http"):
        url = "https://" + url

    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "started", "result": None, "job_type": job_type}

    # Launch Playwright job in a background thread
    Thread(target=run_playwright_job, args=(job_id, job_type, url, params), daemon=True).start()

    return jsonify({"job_id": job_id, "status": "started", "job_type": job_type, "output": None}), 202

@app.route("/status/<job_id>", methods=["GET"])
def job_status(job_id):
    """Check job progress or result."""
    job = jobs.get(job_id)
    if not job:
        return jsonify({"error": "not found"}), 404
    return jsonify(job)

@app.route("/jobs", methods=["GET"])
def list_jobs():
    return jsonify(jobs)

#--------------------------------------------------------------------

def run_playwright_job(job_id, job_type, url, params):
    """Main dispatcher for Playwright jobs."""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=60000)

            # Dispatch job based on job_type
            if job_type == "screenshot":
                result = take_screenshot(page, job_id)

            elif job_type == "click_button":
                result = click_button(page, params)
            else:
                raise ValueError(f"Unknown job_type: {job_type}")

            browser.close()

        jobs[job_id].update({
            "status": "done",
            "result": result or {},
            "output": result,
            })

    except Exception as e:
        jobs[job_id]["status"] = "error"
        jobs[job_id]["error"] = str(e)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

