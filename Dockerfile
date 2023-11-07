# Use base shared Python image
FROM python:3.9

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools wheel

COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Copy the project files into the container
COPY ./src /src

RUN MKDIR ./logs/

# Expose any necessary ports
EXPOSE 8000
EXPOSE 8501

# Set the working directory
WORKDIR /src

# Start the application
CMD ["sh", "-c", "streamlit run UI/ui.py & uvicorn app.main:app --host 0.0.0.0 --port 8000"]