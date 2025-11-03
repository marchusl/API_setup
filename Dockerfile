FROM mcr.microsoft.com/playwright/python:latest
WORKDIR /PlaywrightMain

COPY requirements.txt /PlaywrightMain/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install browsers explicitly
RUN playwright install --with-deps

COPY . /PlaywrightMain

ENV PORT=10000
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "PlaywrightMain:app", "--workers", "1", "--threads", "2"]
