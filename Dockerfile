FROM python:3.10-slim

# Update package lists (executed only when base image version changes)
RUN apt-get update

WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies and system packages
RUN apt-get install -y --no-install-recommends gcc \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get remove --purge -y gcc && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Copy project files (excluding requirements.txt)
COPY . .

# Download NLTK resources
RUN python -c "import nltk; nltk.download('punkt')"

# Command to run
CMD ["python", "test_model.py"]