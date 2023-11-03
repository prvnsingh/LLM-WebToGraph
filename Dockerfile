# Use base shared Python image
FROM python:3.9

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools wheel

COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir --use-pep517 -r /requirements.txt

# Copy the project files into the container
COPY ./src /src



# Expose any necessary ports
EXPOSE 8000

# Set the working directory
WORKDIR /src

# Start the application
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "app.main:app"]