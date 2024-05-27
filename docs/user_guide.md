# User Guide

## Configuration

### Environment Variables

| ENV           | Default       | Description                     |
|---------------|---------------|---------------------------------|
| TEAL_LOG_CONF | log_conf.yaml | The python logging conf (yaml)  |
| TEAL_WORKERS  | 1             | The number of worker processes. |
| TEAL_PORT     | 8000          | Bind socket to this port        |
| TEAL_IP_BIND  | 0.0.0.0       | Bind socket to this host.       |

### Feature flags

You can disable different features in teal with the env `TEA_FEATURE_<PATH>`. For example to disable the libreoffice
feature (`/convert/libreoffice`) you can set `TEA_FEATURE_CONVERT_LIBREOFFICE=false`.