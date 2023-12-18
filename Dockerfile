FROM python:3.11.4-slim-bullseye

# Install system dependencies
RUN apt-get update && \
    apt-get install -y gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==1.4.2

# Configuring poetry
RUN poetry config virtualenvs.create false

# Setting up the working directory

# Copying project files
COPY pyproject.toml poetry.lock ./

# Install project dependencies
RUN poetry install --no-dev

# Copying the project source code
COPY . .

# Expose port 80
EXPOSE 80

# Run the application
CMD ["poetry", "run", "python", "-m", "modelhub"]
