# Teal - A Convenient REST API for Working with PDFs

**Teal** is a versatile and user-friendly API designed to simplify working with PDF documents. Whether you're a
developer looking to automate PDF processing or integrate PDF functionalities into your existing workflow, Teal provides
a seamless and efficient solution.

## Key Features

- Digitize documents to searchable PDF or archivable PDF/A.
- Extract metadata, text, and tables as structured data.
- Convert different document types to PDF.
- Convert PDFs to PDF/A.
- Check PDF/A compliance.

## Getting Started

### Running Teal in App Mode

Here's a quick example of how easy it is to work with Teal:

```bash
docker run --pull=always --rm -it -p 8000:8000 --name teal ghcr.io/rueedlinger/teal:latest
```

Next you can use the api with the openapi ui.

- http://127.0.0.1:8000/docs

### Running Teal in Test Mode

Teal is packed with unit and integration tests. These tests can be run and verified with the following command.

```bash
docker run --pull=always --rm -it -p 8000:8000 -e TEAL_TEST_MODE=true --name teal ghcr.io/rueedlinger/teal:latest
```

### Starting Teal with Locust (Load Testing)

Teal also includes Locust load tests. The following command will start the Locust web UI inside the Docker container.

```bash
docker run --pull=always --rm -it -p 8089:8089 -p 8000:8000 -e TEAL_START_LOCUST=true --name teal ghcr.io/rueedlinger/teal:latest
```

You can now start the load test from the locust webui (http://0.0.0.0:8089/).

## Documentation

see https://teal.yax.ch/



