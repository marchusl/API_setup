def click_button(page, params):
    """
    Clicks a button or element specified by CSS selector.
    Example params: {"selector": "#login-button"}
    """
    selector = params.get("selector")
    if not selector:
        raise ValueError("Missing required param: 'selector'")

    element = page.query_selector(selector)
    if not element:
        raise ValueError(f"Element not found: {selector}")

    element.click()
    return {"message": f"Clicked element '{selector}' successfully"}