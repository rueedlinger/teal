# User Guide

## Running Teal

Here's a quick example of how easy it is to work with Teal directly with docker

```bash
docker run --rm -it -p 8000:8000 -e TEAL_WORKERS=1 --name teal ghcr.io/rueedlinger/teal:main
```

or start Teak inside docker compose.

```yaml
services:
  teal:
    image: ghcr.io/rueedlinger/teal:main
    ports:
      - 8000:8000
    environment:
      #TEAL_LOG_CONF: "log_conf.yaml"
      TEAL_WORKERS: 1
      TEAL_PORT: 8000
      TEAL_IP_BIND: 0.0.0.0
```

## OpenAPI Documentation

Explore the comprehensive OpenAPI documentation for the API at the following links:

- http://localhost:8000/docs
- http://localhost:8000/openapi.json

These resources provide detailed information about the endpoints, request parameters, and response formats.

## Configuration

### Environment Variables

| ENV           | Default       | Description                     |
|---------------|---------------|---------------------------------|
| TEAL_LOG_CONF | log_conf.yaml | The python logging conf (yaml)  |
| TEAL_WORKERS  | 1             | The number of worker processes. |
| TEAL_PORT     | 8000          | Bind socket to this port        |
| TEAL_IP_BIND  | 0.0.0.0       | Bind socket to this host.       |

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

You can disable different features in Teal with the env `TEA_FEATURE_<PATH>`. For example to disable the libreoffice
endpoint path (`/libreoffice/convert`) you can set `TEA_FEATURE_LIBREOFFICE_CONVERT=false`.
