# Use the official Python image.
FROM python:3.12-slim

# Prevent Python from writing pyc files to disc and enable output buffering.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Poetry.
RUN pip install poetry

# Set the working directory.
WORKDIR /app

# Copy dependency files.
COPY pyproject.toml poetry.lock* ./

# Install only production dependencies.
RUN poetry install --no-root --only main

# Copy the project code including the frontend.
COPY . .
COPY frontend ./frontend

# Expose port 8000.
EXPOSE 8000

# Run the API server.
CMD ["poetry", "run", "uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]