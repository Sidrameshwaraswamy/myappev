# Use official Python image
FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy all files to the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask will run on
EXPOSE 5000

# Run the Flask app

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:$PORT", "app:app"]
