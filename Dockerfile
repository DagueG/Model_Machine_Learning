FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY pyproject.toml uv.lock* ./

# Install uv and dependencies from pyproject.toml
RUN pip install uv && uv sync --system

# Copy application (model will be downloaded at runtime)
COPY app ./app
COPY create_db.py .
RUN mkdir -p models

# Initialize database
RUN python create_db.py

# Expose port
EXPOSE 7860

# Run FastAPI with uvicorn on port 7860 (HF Spaces standard)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
