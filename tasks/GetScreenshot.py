
def take_screenshot(page, job_id):
    """Takes a full-page screenshot and saves it."""
    filepath = f"static/screenshots/{job_id}.png"
    page.screenshot(path=filepath, full_page=True)

    return {"screenshot_url": filepath}