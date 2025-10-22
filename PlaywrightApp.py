from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
import base64

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Flask + Playwright API is running on Render!"

@app.route("/run", methods=["POST"])
def run_playwright_direct():
    data = request.get_json(force=True)
    url = data.get("url")
    if not url:
        return jsonify({"error": "missing url"}), 400

    # Ensure URL includes scheme (http/https)
    if not url.startswith("http"):
        url = "https://" + url

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=30000)
            image_bytes = page.screenshot(full_page=True)
            browser.close()

        # Convert to base64 so it's JSON-safe
        image_base64 = base64.b64encode(image_bytes).decode("ascii")
        return jsonify({
            "status": "done",
            "url": url,
            "screenshot_base64": image_base64
        })

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500