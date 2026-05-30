# Prometheus: Ecosystem & Architecture

> 2020-04-06

Prometheus monitoring architecture — core components, data flow, and the network monitoring stack.

## Ecosystem Architecture

![Prometheus Architecture](../../images/prometheus-architecture.png)

**Basic flow:**

1. Prometheus Server scrapes metrics from instrumented **Jobs / Exporters**
2. Server also ingests from the **Pushgateway** for short-lived job metrics
3. Metrics stored locally; rule evaluation produces aggregated time-series data or triggers alerts
4. **Grafana** dashboards visualize time-series data
5. Alertmanager handles alert routing, deduplication, and notification

## Core Components

| Component | Role |
|---|---|
| **Prometheus Server** | Scrapes, stores, evaluates rules |
| **Exporters** | Expose metrics from third-party systems as Prometheus metrics |
| **Pushgateway** | Accepts pushed metrics from short-lived jobs |
| **Alertmanager** | Alert deduplication, grouping, routing |
| **Grafana** | Dashboard visualization |

## Monitoring Stack (Production)

```

Prometheus + M3DB + Nginx + LVS

```

- **M3DB** — Scalable time-series storage backend
- **Nginx + LVS** — Load-balanced access to Prometheus and visualization tier

## References

- [prometheus.io](https://prometheus.io)
