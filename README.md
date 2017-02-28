# alooma-monitor
Feed Alooma Metrics into Datadog

# Maturity 

This is super v.alpha software. Use at your own risk.

# Usage

Requires 3 environment variables be passed into the container.

```
ALOOMA_USERNAME=xxx@xxx.com
ALOOMA_PASSWORD=xxx
DATADOG_API_KEY=xxx
```

From then, polls every 3 minutes and pushes metrics into datadog under an `alooma` top-level namespace.
