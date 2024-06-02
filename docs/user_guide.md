# User Guide

## Running Teal

Here's a quick example of how easy it is to work with Teal directly with docker

```bash
docker run --pull=always --rm -it -p 8000:8000 -e TEAL_WORKERS=1 \
  --name teal ghcr.io/rueedlinger/teal:main
```

or start Teal inside docker compose.

```yaml
services:
  teal:
    image: ghcr.io/rueedlinger/teal:main
    ports:
      - 8000:8000 # Rest API port 
      - 8089:8089 # Locust web ui port
    environment:
      TEAL_LOG_CONF: "log_conf.yaml"
      # TEAL_WORKERS: 1
      # TEAL_WORKERS_TIMEOUT: 90
      TEAL_PORT: 8000
      # TEAL_IP_BIND: 0.0.0.0
      # TEAL_START_LOCUST: 'true'
```

## OpenAPI Documentation

Explore the comprehensive OpenAPI documentation for the API at the following links:

- [http://localhost:8000/docs](http://localhost:8000/docs)
- [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

These resources provide detailed information about the endpoints, request parameters, and response formats.

## Configuration

### Environment Variables

| ENV                  | Default       | Description                                                                                 |
|----------------------|---------------|---------------------------------------------------------------------------------------------|
| TEAL_LOG_CONF        | log_conf.yaml | The python logging conf yaml file.                                                          |
| TEAL_WORKERS         | 1             | The number of worker processes. Number of recommended workers is 2 x number_of_cores + 1.   |
| TEAL_WORKERS_TIMEOUT | 120           | Worker timeout in seconds.                                                                  |
| TEAL_PORT            | 8000          | Bind socket to this port                                                                    |
| TEAL_IP_BIND         | 0.0.0.0       | Bind socket to this host.                                                                   |
| TEAL_START_LOCUST    | false         | When set to to `true`, the locust will be started. The web ui can be accessed on port 8089. |

### Logging

With `TEAL_LOG_CONF` environment variable to can specif a logging configuration yaml file for Teal.

```yaml
version: 1
disable_existing_loggers: False

formatters:
  simple:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    datefmt: '%Y-%m-%d %H:%M:%S'

handlers:
  console:
    class: logging.StreamHandler
    formatter: simple
    stream: ext://sys.stdout

  # file:
  #    class: logging.FileHandler
  #    formatter: simple
  #    filename: myapp.log
  #    mode: a

loggers:
  teal:
    level: INFO
    handlers: [ console ]
    propagate: yes
  uvicorn.error:
    level: INFO
    handlers: [ console ]
    propagate: no
  uvicorn.access:
    level: INFO
    handlers: [ console ]
    propagate: no

root:
  handlers: [ console ]
  level: WARN
```

### Feature Flags

You can disable different features in Teal with the env `TEAL_FEATURE_<PATH>`. For example to disable the libreoffice
endpoint path (`/libreoffice/convert`) you can set `TEAL_FEATURE_LIBREOFFICE_CONVERT=false`.

Currently there are the following feature flags:

- TEAL_FEATURE_PDF_TEXT
- TEAL_FEATURE_PDF_OCR
- TEAL_FEATURE_PDF_TABLE
- TEAL_FEATURE_PDFA_CONVERT
- TEAL_FEATURE_PDFA_VALIDATE
- TEAL_FEATURE_LIBREOFFICE_CONVERT
- TEAL_FEATURE_HEALTH
- TEAL_FEATURE_METRICS