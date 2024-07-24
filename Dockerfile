# Use the official Python runtime as a parent image
FROM python:3.7.2-alpine3.9

# Set the working directory to /usr/src/app
WORKDIR /usr/src/app

# Copy the local code directory into the container at /usr/src/app
#COPY ./code /usr/src/app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir openai requests

# Define the command to run your Python script
CMD ["python", "aicodesuggestions.py"]


#test