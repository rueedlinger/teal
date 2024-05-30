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

## Unit/Integration Testing

To run the pytest inside the docker container just pass the env `TEAL_TEST_MODE=true`. When you want to pass
arguments to pytest you can use the env `TEAL_PYTEST_ARGS`.

```bash
docker compose run --build --name teal_pytest --rm -e TEAL_TEST_MODE=true teal
```

## Load Testing

You can run the load test locally or inside docker.

### Locally

The following command will start the load test with locust.

```bash
locust --host http://localhost:8000 --users 5 -t 10m --autostart -f tests/locustfile.py
```

You can see the result with the locust webui (http://0.0.0.0:8089/).

### Inside Docker

The following command will start the locust webui inside the docker container.

```bash
docker compose run --build --rm -p 8089:8089 -p 8000:8000 -e TEAL_START_LOCUST=true teal
```

You can now start the load test from the locust webui (http://0.0.0.0:8089/).

### Result

The following is load test run with 5 users for 10 minutes (10 workers, worker timeout 120 seconds)
on a mac book pro (2023, Apple M2 Max, 64GB Mem) witch docker settings memory limit 16GB and CPU limit 12.

| Type | Name                 | # Requests | # Fails | Median (ms) | 95%ile (ms) | 99%ile (ms) | Average (ms) | Min (ms) | Max (ms) | Average size (bytes) | Current RPS | Current Failures/s |
|------|----------------------|------------|---------|-------------|-------------|-------------|--------------|----------|----------|----------------------|-------------|--------------------|
| POST | /libreoffice/convert | 370        | 0       | 620         | 750         | 940         | 628.05       | 514      | 1197     | 59527.49             | 0.5         | 0                  |
| POST | /pdf/ocr             | 326        | 0       | 6100        | 8100        | 9400        | 6198.9       | 4101     | 10376    | 5009                 | 0.8         | 0                  |
| POST | /pdf/table           | 342        | 0       | 590         | 690         | 730         | 607.71       | 553      | 808      | 154                  | 0.5         | 0                  |
| POST | /pdf/text            | 336        | 0       | 9           | 18          | 22          | 9.87         | 6        | 84       | 5169                 | 1           | 0                  |
| POST | /pdfa/convert        | 335        | 0       | 360         | 440         | 480         | 367.51       | 316      | 812      | 51695                | 0.6         | 0                  |
| POST | /pdfa/validate       | 346        | 0       | 1100        | 1300        | 1400        | 1145.63      | 864      | 1543     | 214                  | 0.4         | 0                  |
|      | Aggregated           | 2055       | 0       | 600         | 6600        | 7900        | 1452.01      | 6        | 10376    | 20846.44             | 3.8         | 0                  |

