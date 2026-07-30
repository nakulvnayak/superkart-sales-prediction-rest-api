
FROM python:3.9-slim

# Set the working directory inside the container to /app
WORKDIR /app

# Copy all files from the current directory on the host to the container's /app directory
COPY . .

# Install Python dependencies listed in requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Document the port used by Gunicorn
EXPOSE 7860

# Start the Flask application using Gunicorn
CMD ["gunicorn","-w","4","-b","0.0.0.0:7860","app:superkart_predictor_api"]
