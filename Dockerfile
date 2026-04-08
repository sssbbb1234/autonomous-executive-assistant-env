# Use Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir \
    pydantic \
    openai

# Expose port (HF requirement)
EXPOSE 7860

# Default command
CMD ["python", "inference.py"]