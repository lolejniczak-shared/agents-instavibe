# /Users/linchr/Desktop/work/datecoach/agents/social/Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# --- Dependency Installation ---
# Copy only the requirements file first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt


# --- Application Code ---
COPY ./ /app/agents/planner

# --- Environment ---
ENV PYTHONPATH=/app/agents 


# Make port 8080 available to the world outside this container
# Cloud Run uses the PORT env var, but EXPOSE is good practice.
EXPOSE 8080

# --- Run the application ---
# Run a2a_server.py when the container launches
# Use the module execution '-m' which works well with the PYTHONPATH setup
CMD ["python", "/app/agents/planner/a2a_server.py"]
