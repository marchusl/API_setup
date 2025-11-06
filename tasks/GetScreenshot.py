def take_screenshot(page, job_id):
    filepath = f"static/screenshots/{job_id}.png"
    page.screenshot(path=filepath, full_page=True)

    screenshot_url = f"https://api-setup-nd3w.onrender.com/static/screenshots/{job_id}.png"
    return {screenshot_url}
