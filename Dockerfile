FROM python:3.11-slim

# Create a non-root user specifically for HF Spaces
RUN useradd -m -u 1000 user

WORKDIR /app

# Install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy files and set ownership
COPY --chown=user:user . .

USER user
EXPOSE 7860

# Start server
CMD ["python", "-m", "app.main"]
