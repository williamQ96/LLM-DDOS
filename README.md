# LLM-DDOS: AI-Orchestrated Distributed Denial-of-Service Simulation

A research-focused simulation system that uses Large Language Models (LLMs) to autonomously orchestrate and simulate DDoS attacks. This project demonstrates how AI agents can coordinate observation, analysis, and attacks in a distributed architecture.

## 🧠 Project Structure

- **Commander Node**: Observes the target, analyzes network status using an LLM (Mistral), and issues strategy commands via Redis pub/sub.
- **Ninja Nodes**: Subscribe to the commander’s channel, receive attack instructions, and execute simulated DDoS attacks (e.g., SYN flood, HTTP flood, Slowloris) using external tools or internal scripts.
- **Target**: A mock or live endpoint being monitored and attacked for research and testing purposes.

## 📂 Directory Structure
```text
C:.
│   docker-compose.yml
│   ninja_1.log
│   output.txt
│   README.md
│   Slides.pdf
│   ui_console.log
│
├── attack
│   ├── http_flood.py
│   ├── slowloris.py
│   ├── tcp_flood.py
│   └── __pycache__
│       ├── http_flood.cpython-312.pyc
│       ├── slowloris.cpython-312.pyc
│       └── tcp_flood.cpython-312.pyc
│
├── images
│   └── ollama_output.png
│
├── infra
│   ├── monitor.py
│   ├── pubsub.py
│   └── __pycache__
│       ├── monitor.cpython-312.pyc
│       └── pubsub.cpython-312.pyc
│
├── llm
│   ├── prompt_templates.py
│   ├── finetune_config
│   └── __pycache__
│       └── prompt_templates.cpython-312.pyc
│
├── log
│   ├── commander_1.log
│   ├── console.log
│   └── ninja_1a.log
│
├── nodes
│   ├── commander.py
│   ├── commander_ai.py
│   └── ninja.py
│
├── scripts
│   └── fake_traffic.py
│
└── ui
    ├── control_panel.py
    └── print_log.py
``` 
---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Docker (for Redis)
- [Ollama](https://ollama.com/) with Mistral model loaded(or any LLM model depends on your capacity and configurtion)

## Installation

### Clone the repo
git clone https://github.com/williamq96/LLM-DDOS.git
cd LLM-DDOS

### Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

### Install Python dependencies
```
pip install -r requirements.txt
```
### Start Redis using Docker
```
docker compose up -d
```
## 🚀 Running the Simulation

### Start the Commander AI
```
python nodes/commander_ai.py --name commander-1 --channel commander-1-channel
```

### Start a Ninja Node
```
python nodes/ninja_node.py --name ninja-1 --channel commander-1-channel
```
You can run multiple Ninja nodes concurrently to simulate a distributed botnet.

## ⚙️ Configuration
Change channel names and loop intervals in the scripts as needed.

Modify llm/prompt_templates.py to adjust system prompts for the Commander.

## 📈 Research Goals
### Showcase autonomous agent behavior in coordinated attacks.

### Compare performance between different LLMs for tactical decisions.

### Explore mitigation strategies and defense against adaptive AI-based attacks.

## ⚠️ Disclaimer
This project is intended for educational and research purposes only. Do not use it to perform unauthorized attacks on real systems. Always test in controlled environments.

## 📄 License
MIT License