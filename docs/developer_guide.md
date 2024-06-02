# Developer Guide

## Python

### Install Python 3.12.0 Using pyenv

This command will download and install Python version 3.12.0. Pyenv is a popular tool for managing multiple versions of
Python on a single system.

```bash
pyenv install 3.12.0
```

### Create a Virtual Environment Named 'teal'

This command will create a virtual environment using the Python version 3.12.0 that was just installed. Virtual
environments are useful for managing project-specific dependencies.

```bash
pyenv virtualenv 3.12.0 teal
```

### Activate the Virtual Environment 'teal'

Activating the virtual environment ensures that any Python commands run will use the packages and interpreter from the '
teal' environment.

```bash
pyenv activate teal
```

### Install Dependencies from requirements.txt

This command will install all the necessary packages listed in the requirements.txt file. This file typically contains a
list of all the Python packages required for the project.

```bash
pip install -r requirements.in
```

### Update Dependencies

To update the dependencies, first modify the `requirements.in` file with the desired package versions or additions.
Then, run the following command to generate an updated requirements.txt file:

```bash
pip-compile --output-file=requirements.txt
```

This will ensure that the requirements.txt file is synchronized with the changes made in requirements.in.

> *Note:* *pip-compile* is a tool from the pip-tools package. If you don't have it installed, you can add it using pip
> install pip-tools. For more information, visit
> the [pip-tools documentation](https://pip-tools.readthedocs.io/en/stable/).

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

To run pytest inside the Docker container, set the environment variable `TEAL_TEST_MODE=true`. If you need to pass
arguments to pytest, you can use the `TEAL_PYTEST_ARGS` environment variable.

To run pytest without additional arguments, use the following command:

```bash
docker compose run --build --name teal_pytest \
  --rm -e TEAL_TEST_MODE=true teal
```

If you need to pass arguments to pytest, set the `TEAL_PYTEST_ARGS` environment variable. For example, to run tests in
verbose mode, you can use:

```bash
docker compose run --build --name teal_pytest \
  --rm -e TEAL_TEST_MODE=true -e TEAL_PYTEST_ARGS="-v" teal
```

## Load Testing

You can run the load test locally or inside a Docker container.

### Locally

The following command will start the load test with Locust. Note that the application must be running on port 8000 when
you start the load test.

```bash
locust --host http://localhost:8000 --users 5 -t 10m \
  --autostart -f tests/locustfile.py
```

You can view the results with the Locust web UI at http://0.0.0.0:8089/.

### Inside Docker

The following command will start the Locust web UI inside the Docker container:

```bash
docker compose run --build --rm -p 8089:8089 -p 8000:8000 \
  -e TEAL_START_LOCUST=true teal
```

The -e `TEAL_START_LOCUST=true` environment variable signals the container to start Locust.

You can now start the load test from the Locust web UI, accessible at http://0.0.0.0:8089/. To begin, navigate to this
URL in your web browser. From the interface, you can configure various test parameters such as the number of users,
spawn rate, and duration of the test. Once your settings are in place, click the "Start" button to initiate the load
test. As the test runs, you can monitor real-time performance metrics and view detailed statistics on response times,
failure rates, and other key indicators. This will help you assess the performance and stability of your application
under load.

### Result

The test was performed on a MacBook Pro (2023 model, Apple M2 Max, 64GB
RAM). Docker settings were configured with a memory limit of 16GB and a CPU limit of 12 cores. Please note that the
results obtained from this test may vary based on differences in hardware and software configurations in your setup.

The following load test was conducted with 5 user for a duration of 10 minutes. The test configuration included 1
worker with a timeout of 120 seconds. The PDF document used for all test has a size of 17 KB (16'873 bytes, one page).

| Type           | Name                 | # Requests | # Fails | Median (ms) | 95%ile (ms) | 99%ile (ms) | Average (ms) | Min (ms) | Max (ms)  | Average size (bytes) | Current RPS | Current Failures/s |
|----------------|----------------------|------------|---------|-------------|-------------|-------------|--------------|----------|-----------|----------------------|-------------|--------------------|
| POST           | /libreoffice/convert | 191        | 0       | 4600        | 8800        | 10000       | 4766.63      | 500      | 12394     | 21297                | 0.2         | 0                  |
| POST           | /pdf/ocr             | 209        | 0       | 1400        | 2600        | 2800        | 1509.29      | 684      | 3499      | 635                  | 0.5         | 0                  |
| POST           | /pdf/table           | 212        | 0       | 1300        | 2400        | 2600        | 1370.22      | 558      | 2955      | 2                    | 0.1         | 0                  |
| POST           | /pdf/text            | 223        | 0       | 780         | 2000        | 2300        | 783.64       | 2        | 2740      | 654                  | 0.4         | 0                  |
| POST           | /pdfa/convert        | 197        | 0       | 4600        | 9300        | 11000       | 4845.74      | 305      | 11176     | 21436                | 0.2         | 0                  |
| POST           | /pdfa/validate       | 213        | 0       | 1500        | 2500        | 3000        | 1522.62      | 767      | 3499      | 171                  | 0.5         | 0                  |
| **Aggregated** |                      | **1245**   | **0**   | **1600**    | **6900**    | **9500**    | **2385.57**  | **2**    | **12394** | **6912.47**          | **1.9**     | **0**              |
