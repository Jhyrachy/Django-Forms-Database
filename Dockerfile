# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container; directory del progetto
WORKDIR /bologna

# Copia il progetto nella cartella selezionata sopra
COPY . /bologna

# Install any necessary dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV DJANGO_ENV=development

# Run the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]