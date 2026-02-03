FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY webhook/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy webhook code
COPY webhook/stripe_webhook.py .

# Expose port
EXPOSE 5000

# Run webhook server
CMD ["python", "stripe_webhook.py"]
