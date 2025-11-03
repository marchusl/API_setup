import os

def take_screenshot(page, job_id):
    filepath = f"static/screenshots/{job_id}.png"
    page.screenshot(path=filepath, full_page=True)

    public_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME', 'localhost')}/static/screenshots/{job_id}.png"
    return {"screenshot_url": "https://yourapp.com/static/screenshots/<job_id>.png"}
