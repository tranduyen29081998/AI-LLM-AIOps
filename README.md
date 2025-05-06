# Chatbot LLM with Prometheus & Grafana Monitoring

This project builds a simple chatbot using `GPT-Neo 125M`, exposes response time metrics via Prometheus, and visualizes them in Grafana. You can also configure alerts directly in the Grafana UI.

## 🚀 Getting Started

### 1. Clone & Build Docker

```bash
git clone https://github.com/tranduyen29081998/AI-LLM-AIOps.git
cd AI-LLM-AIOps
docker-compose up --build
```

### 2. Services Overview

- `http://localhost:5000/chat`: Chatbot API (POST)
- `http://localhost:8000/metrics`: Prometheus metrics
- `http://localhost:9090`: Prometheus UI
- `http://localhost:3000`: Grafana (admin / admin)

## 🔧 Flask + Metrics

Metrics are exposed via Prometheus client on port `8000`:

```python
from prometheus_client import Gauge, start_http_server

response_time = Gauge('response_time_seconds', 'Time taken to generate response in seconds')

@app.route("/chat", methods=["POST"])
def chat():
    start = time.time()
    ...
    response_time.set(end - start)
```

## 📈 Monitoring Stack (Docker Compose)

```yaml
version: "3.8"
services:
  chatbot:
    build: .
    ports:
      - "5000:5000"
      - "8000:8000"
    networks: [monitor-net]

  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports: ["9090:9090"]
    networks: [monitor-net]

  grafana:
    image: grafana/grafana
    ports: ["3000:3000"]
    volumes:
      - grafana-storage:/var/lib/grafana
    networks: [monitor-net]

volumes:
  grafana-storage:
networks:
  monitor-net:
```

### Prometheus Config (`prometheus.yml`)

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: "chatbot"
    static_configs:
      - targets: ["chatbot:8000"]
```

## 🔔 Alerting Setup

Alert rules are created **directly in Grafana UI**:

1. Go to **Alerting → Alert Rules**
2. Create a new rule:
   - Query: `response_time_seconds`
   - Condition: `is above 2`
   - Evaluation: every 30s
   - Add Slack/email contact point

> ⚠️ Ensure Slack or SMTP is set up in **Alerting → Contact points**

## 🧠 Model

- Model: [EleutherAI/gpt-neo-125M](https://huggingface.co/EleutherAI/gpt-neo-125M)
- Inference is handled via `transformers` with a basic generation pipeline

## ☁️ Deployment

You can deploy this stack to AWS EC2 (e.g., t2.medium) or GCP Compute Engine. Just install Docker & Docker Compose, clone the repo, and run:

```bash
docker-compose up -d
```

Ensure ports `5000`, `8000`, `9090`, and `3000` are open in the firewall.
