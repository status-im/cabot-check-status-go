# Description

This is a [Cabot Check Plugin](https://cabotapp.com/dev/writing-check-plugins.html) for running a [status-go](https://github.com/status-im/status-go) canary.

# Installation

The simplest way is to just use:
```sh
pip install git+git://github.com/status-im/cabot-check-status-go.git
```
Edit conf/production.env in your Cabot clone to include the plugin:
```
CABOT_PLUGINS_ENABLED=cabot_check_status_go,<other plugins>
```

# Configuration

This plugin requries one environment variable:
```sh
STATUS_GO_CANARY_PATH=<path_to_status_go_canary_binary>
```
