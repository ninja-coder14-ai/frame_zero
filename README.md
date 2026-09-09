# Frame Zero - AI Anomaly Investigator

## What It Does

Frame Zero is an AI agent that automatically investigates anomalies in media production pipelines using Grafana logs. It queries Loki logs, analyzes issues, and creates annotations in Grafana.

## How It Works

1. User asks the agent to investigate an anomaly
2. Agent queries Grafana/Loki for relevant logs
3. Agent analyzes the results in one pass
4. If anomaly found, creates a Grafana annotation
5. Returns findings to the user

## Setup

### Install Dependencies
```bash
pip install google-adk google-genai mcp uvx
```

### Set Environment Variables
```bash
export GRAFANA_URL="your-grafana-url"
export GRAFANA_SERVICE_ACCOUNT_TOKEN="your-token"
```

## Usage

```python
from main import root_agent

response = root_agent.run("Investigate anomalies in the media production pipeline")
print(response)
```

## Technologies

- Google ADK (Agent Development Kit)
- Gemini AI Model
- Grafana + Loki
- MCP Tools

## Team

Hackathon Submission 2026
