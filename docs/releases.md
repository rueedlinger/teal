# Releases

## Versions

| Version | Docker                          | Description        |
|---------|---------------------------------|--------------------|
| main    | ghcr.io/rueedlinger/teal:main   | Latest main branch |
| v0.1.0  | ghcr.io/rueedlinger/teal:v0.1.0 | Initial release    |

These are the available releases and their corresponding Docker images for the 'teal' project.

## Known Issues

### Extract Tables (/pdf/table ) - Ignoring wrong pointing object

The following warning is displayed when extracting tables from a PDF. The extraction works, but this warning is
displayed:

```
pypdf._reader - WARNING - Ignoring wrong pointing object 6 0 (offset 0)
```

This warning typically indicates that the PyPDF library encountered an object in the PDF that it couldn't interpret
correctly. Despite this, the extraction process completes successfully. This warning may not impact the extracted data
but suggests that there might be some issues with the PDF's structure or content.

### Metrics - CPU and MEM metrics not available with multiworker

This is unrelated to trallnag/prometheus-fastapi-instrumentator. The official Prometheus client library for Python does
not include these metrics when multi process mode is enabled.

see [https://github.com/trallnag/prometheus-fastapi-instrumentator/issues/207](https://github.com/trallnag/prometheus-fastapi-instrumentator/issues/207)