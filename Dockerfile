FROM python:3.11-slim
WORKDIR /app
COPY gisn.py tests/ ./
RUN pip install --no-cache-dir numpy psutil
CMD ["python", "tests/stress_1M.py"]
