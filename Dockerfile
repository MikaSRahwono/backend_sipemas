FROM python:3.11.8

# Install dependencies
RUN apt-get update -qq && apt-get install -y -qq \
    gdal-bin binutils libproj-dev libgdal-dev cmake && \
    apt-get clean all && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /var/cache/apt/*

RUN apt-get update \
    && apt-get install -y postgresql-client \
    && rm -rf /var/lib/apt/lists/*


# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /backend_sipemas

# Copy only the requirements file first to leverage Docker cache
COPY backend_sipemas/requirements.txt /backend_sipemas/requirements.txt

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY backend_sipemas /backend_sipemas

# Copy the entrypoint script and make it executable
COPY backend_sipemas/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Specify the entrypoint
ENTRYPOINT ["/entrypoint.sh"]
