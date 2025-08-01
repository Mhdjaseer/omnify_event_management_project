# Use official Python image
FROM python:3.11-slim

# Prevent .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy source code
COPY . .

# Run development server comment this for production
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] 
# uncomment this for production
# CMD ["gunicorn", "event_manager.wsgi:application", "--bind", "0.0.0.0:8000"] 