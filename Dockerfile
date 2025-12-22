FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY pyproject.toml uv.lock* ./

# Install uv and dependencies
RUN pip install uv && uv pip install --system -r requirements.txt 2>/dev/null || \
    (pip install fastapi uvicorn pydantic python-dotenv joblib scikit-learn pandas sqlalchemy)

# Copy application
COPY app ./app
COPY models ./models
COPY create_db.py .

# Initialize database
RUN python create_db.py

# Expose port
EXPOSE 7860

# Run FastAPI with uvicorn on port 7860 (HF Spaces standard)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
