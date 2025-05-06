FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . .

# Expose the ports for Flask app and Prometheus metrics
EXPOSE 5000 8000

# Run the Flask app with gunicorn and expose Prometheus metrics
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
