# Use the official Python runtime as a parent image
FROM python:3.7.2-alpine3.9

# Install bash
RUN apk add --no-cache bash

# Set the working directory to /usr/src/app
WORKDIR /usr/src/app

# Copy the local code directory into the container at /usr/src/app
#COPY ./code /usr/src/app #we are mounting this in rundocker instead

RUN pip install --upgrade pip 

#install requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Define the command to run your Python script
CMD ["python", "aicodesuggestions.py"]

