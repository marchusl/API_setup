# Dockerfile
FROM mcr.microsoft.com/playwright/python:latest

# Create app directory
WORKDIR /PlaywrightApp

# Copy only what's needed for caching
COPY requirements.txt /PlaywrightApp/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy app code
COPY . /PlaywrightApp

# If you need to install any additional Playwright browsers, you can:
# RUN playwright install --with-deps
# But the base image typically includes browsers already.

# Use gunicorn for production (bind to PORT from Render)
ENV PORT=10000
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app", "--workers", "1", "--threads", "2"]