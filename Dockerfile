# Use base shared Python image
FROM python:3.8

RUN pip3 install --upgrade pip

COPY ./requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

# Copy the project files into the container
COPY ./src /src



# Expose any necessary ports
EXPOSE 8000

# Set the working directory
WORKDIR /src

# Start the application
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "main:app"]