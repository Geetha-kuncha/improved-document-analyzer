FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY structural_document_analyzer.py .
COPY test_analyzer.py .
COPY run_analysis.sh .

# Make shell script executable
RUN chmod +x run_analysis.sh

# Create directories for input and output
RUN mkdir -p /app/documents /app/output

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Default command
CMD ["python3", "structural_document_analyzer.py", "--help"]
