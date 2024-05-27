# Developer Guide

## Python

```bash
pyenv install 3.12.0 
pyenv virtualenv 3.12.0 teal 
pyenv activate teal  
pip install -r requiremnts.txt
```

Start the app.

```bash
uvicorn teal.api:app --reload
```

## Docker Container

To start up the whole app just build and run the container with `docker compose`.

```bash
docker compose up --build
```

## Testing

To run the pytest inside the docker container just pass the env `TEAL_TEST_MODE=true`. When you want to pass
arguments to pytest you can use the env `TEAL_PYTEST_ARGS`.

```bash
docker compose run --build --name teal_pytest --rm -e TEAL_TEST_MODE=true teal
```

## Publish

```bash
docker build . --tag ghcr.io/rueedlinger/teal:latest 
```

```bash
docker push ghcr.io/rueedlinger/teal:latest 
```