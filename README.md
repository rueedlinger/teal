# Teal - A Convenient REST API for Working with PDFs

**Teal** is a versatile and user-friendly API designed to simplify working with PDF documents. Whether you're a
developer looking to automate PDF processing or integrate PDF functionalities into your existing workflow, Teal provides
a seamless and efficient solution.

## Getting Started

### Running Teal in App Mode

Here's a quick example of how easy it is to work with Teal:

```bash
docker run --rm -it -p 8000:8000 --name teal ghcr.io/rueedlinger/teal:latest
```

Next you can use the api with the openapoi ui.

- http://127.0.0.1:8000/docs

### Running Teal in Test Mode

Teal is packed with unit and integration tests. These test can be run and verified with teh following command.

```bash
docker run --rm -it -p 8000:8000 -e TEAL_TEST_MODE=true --name teal ghcr.io/rueedlinger/teal:latest
```

## Documentation

see tbd





