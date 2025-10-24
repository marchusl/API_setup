from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
from threading import Thread
import os, uuid

app = Flask(__name__)
jobs = {}

os.makedirs("static/screenshots", exist_ok=True)

@app.route("/")
def home():
    return "✅ Flask + Playwright API is running on Render!"

def run_playwright_job(job_id, url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)

            filepath = f"static/screenshots/{job_id}.png"
            page.screenshot(path=filepath, full_page=True)
            browser.close()

        jobs[job_id]["status"] = "done"
        jobs[job_id]["screenshot_url"] = (f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME', 'localhost')}/static/screenshots/{job_id}.png")
    
    except Exception as e:
        jobs[job_id]["status"] = "error"
        jobs[job_id]["error"] = str(e)
        jobs[job_id]["screenshot_url"] = "not ready"



@app.route("/run", methods=["POST"])
def start_job():
    data = request.get_json(force=True)
    url = data.get("url")

    if not url:
        return jsonify({"error": "missing url"}), 400

    # Ensure URL includes scheme (http/https)
    if not url.startswith("http"):
        url = "https://" + url

    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "started", "screenshot_url": "not ready"}

    # Launch Playwright job in a background thread
    Thread(target=run_playwright_job, args=(job_id, url), daemon=True).start()

    return jsonify({"job_id": job_id, "status": "started"}), 202

@app.route("/status/<job_id>", methods=["GET"])
def job_status(job_id):
    job = jobs.get(job_id)
    if not job:
        return jsonify({"error": "not found"}), 404
    return jsonify(job)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

