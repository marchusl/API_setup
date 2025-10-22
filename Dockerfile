FROM mcr.microsoft.com/playwright/python:latest
WORKDIR /PlaywrightApp

COPY requirements.txt /PlaywrightApp/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install browsers explicitly
RUN playwright install --with-deps

COPY . /PlaywrightApp

ENV PORT=10000
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "PlaywrightApp:app", "--workers", "1", "--threads", "2"]
