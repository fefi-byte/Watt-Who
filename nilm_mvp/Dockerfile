FROM python:3.11-slim

WORKDIR /app

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy application code and add-on resources from the build context
COPY ./app /app
COPY ./config.yaml ./run.sh ./README.md /addon/

CMD ["/bin/bash", "/addon/run.sh"]
