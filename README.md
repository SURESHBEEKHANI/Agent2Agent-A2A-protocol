# Agent-to-Agent (A2A) Protocol

A collection of projects demonstrating the **Agent-to-Agent (A2A) protocol** for building interoperable AI agents that discover, communicate, and collaborate with each other.

## Overview

This repository contains reference implementations and examples for the A2A protocol—a standard for enabling AI agents to interoperate across different frameworks and vendors. Agents expose their capabilities via **Agent Cards** and communicate through a well-defined request/response model.

## Projects

| Project | Description |
|---------|-------------|
| **[a2a-workflow](./a2a-workflow/)** | A minimal starter: a simple Greeting Agent server and client. Ideal for learning the basics. |
| **[a2a-project](./a2a-project/)** | Multi-agent badminton scheduling system with Elon (orchestrator), Jeff, and Mark agents using Google ADK, LangChain, and CrewAI. |

### a2a-workflow

- **Greeting Agent** – Basic agent that returns a greeting
- **A2A server** – Starlette + Uvicorn
- **Client** – Discovers the agent via Agent Card and sends messages
- **Stack**: `a2a-sdk`, Starlette, Uvicorn

[→ View a2a-workflow README](./a2a-workflow/README.md)

### a2a-project

- **ElonAgent** – Host/orchestrator (Google ADK)
- **JeffAgent** – Jeff’s scheduling assistant (LangGraph)
- **MarkAgent** – Mark’s scheduling assistant (CrewAI)
- **Features**: Multi-agent coordination, scheduling, court booking, conversation memory

[→ View a2a-project README](./a2a-project/README.md)

## Quick Start

### Prerequisites

- Python 3.11+ (a2a-workflow) or Python 3.13+ (a2a-project)
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### a2a-workflow (minimal example)

```bash
cd a2a-workflow
uv sync

# Terminal 1: Start the agent server
uv run -m dummy_agent

# Terminal 2: Run the client
uv run dummy_agent/client.py
```

### a2a-project (multi-agent system)

```bash
cd a2a-project
uv sync

# Set up .env with Groq_API_KEY
# Then start agents (each in its own terminal):
cd jeff_agent && python -m jeff_agent   # Port 10004
cd mark_agent && python -m mark_agent   # Port 10005
cd elon_agent && python agent.py        # Orchestrator
```

## Technology Stack

| Component | Technologies |
|-----------|--------------|
| **Protocol** | A2A SDK, Agent Cards, Agent Skills |
| **Web** | Starlette, Uvicorn, httpx |
| **AI/LLM** | Google ADK, LangChain, LangGraph, CrewAI, LiteLLM, Groq |
| **Tooling** | uv (package manager) |

## Project Structure

```
Agent2Agent-A2A-protocol/
├── a2a-workflow/       # Simple greeting agent demo
│   ├── dummy_agent/    # Server, executor, client
│   ├── pyproject.toml
│   └── README.md
├── a2a-project/        # Multi-agent scheduling system
│   ├── elon_agent/     # Orchestrator
│   ├── jeff_agent/     # LangGraph-based agent
│   ├── mark_agent/     # CrewAI-based agent
│   ├── pyproject.toml
│   └── README.md
└── README.md           # This file
```

## Learn More

- [A2A Specification](https://ai.google.dev/a2a-spec) – Google’s A2A protocol documentation
- [a2a-sdk](https://pypi.org/project/a2a-sdk/) – Python SDK for building A2A agents

## License

[Add your license information here]
