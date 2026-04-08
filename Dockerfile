FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir pydantic

CMD ["bash", "-c", "python inference.py && tail -f /dev/null"]
