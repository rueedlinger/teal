# Developer Guide

## Python

### Install Python 3.12.0 using pyenv

This command will download and install Python version 3.12.0. Pyenv is a popular tool for managing multiple versions of
Python on a single system.

```bash
pyenv install 3.12.0
```

### Create a virtual environment named 'teal'

This command will create a virtual environment using the Python version 3.12.0 that was just installed. Virtual
environments are useful for managing project-specific dependencies.

```bash
pyenv virtualenv 3.12.0 teal
```

### Activate the virtual environment 'teal'

Activating the virtual environment ensures that any Python commands run will use the packages and interpreter from the '
teal' environment.

```bash
pyenv activate teal
```

### Install dependencies from requirements.txt

This command will install all the necessary packages listed in the requirements.txt file. This file typically contains a
list of all the Python packages required for the project.

```bash
pip install -r requirements.txt
```

### Install Binaries

The easiest way is just to run the app inside the Docker container. This approach ensures that all necessary binaries
are included and configured correctly without needing to manage them manually on your local system. Docker containers
provide a consistent and isolated environment, which helps avoid issues related to different operating systems or
library versions.

The following binaries (debian packages) are needed:

- tesseract-ocr
- tesseract-ocr-eng (and additional required languages)
- poppler-utils
- ocrmypdf
- ghostscript
- python3-tk
- libgl1
- libreoffice
- default-jre-headless
- libreoffice-java-common
- jodconverter

The following binaries must be installed manually:

- verapdf

### Startup the FastAPI app

This will start the FastAPI app. BUT Some APIs within the FastAPI application may depend on external binaries or system
packages. Make sure these dependencies are installed and properly configured on your system. For instance, if an API
endpoint requires tesseract or libreoffice, these binaries must be available in your system's PATH.

```bash
uvicorn teal.api:app --reload
```

## Docker

### Starting the App with Docker Compose

To start up the whole app with all libraries and binaries, just build and run the container with Docker Compose. This
approach ensures that the entire application, including all dependencies and necessary binaries, is consistently and
reliably set up in a containerized environment.

To build and run the container, use the following command

```bash
docker compose up --build
```

## Testing

To run the pytest inside the docker container just pass the env `TEAL_TEST_MODE=true`. When you want to pass
arguments to pytest you can use the env `TEAL_PYTEST_ARGS`.

```bash
docker compose run --build --name teal_pytest --rm -e TEAL_TEST_MODE=true teal
```
