FROM python:3.10-slim

# Set up environment
# Prevents .pyc files from being written to the container
ENV PYTHONDONTWRITEBYTECODE=1
# Forces stdout and stderr to be unbuffered
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y build-essential

# Copy app code
COPY . /app

# Install Python deps
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Start command (will run both apps)
CMD ["bash", "start.sh"]
