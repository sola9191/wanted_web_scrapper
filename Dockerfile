# Dockerfile for Render deployment with Playwright support
FROM mcr.microsoft.com/playwright/python:v1.51.0-jammy

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Expose the port Flask will run on
EXPOSE 5000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

# Run the Flask app
CMD ["python", "main.py"]
