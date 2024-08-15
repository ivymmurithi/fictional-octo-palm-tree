# Base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install pipenv
RUN pip install pipenv

# Copy Pipfile and Pipfile.lock first
COPY Pipfile Pipfile.lock /app/

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies using pipenv
RUN pipenv install --deploy --ignore-pipfile

RUN pipenv run pip list

# Copy the rest of the application code
COPY . /app

# Expose the port the app runs on
EXPOSE 8000

# Command to run the Django application
CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
