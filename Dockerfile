# Use official Playwright image (includes all browsers)
FROM mcr.microsoft.com/playwright/python:v1.53.0-jammy

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --upgrade pip && pip install -r backend/requirements.txt

# Set environment variables
ENV PYTHONPATH=/app/backend

# Expose port
EXPOSE 10000

# Run FastAPI app
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "10000"]