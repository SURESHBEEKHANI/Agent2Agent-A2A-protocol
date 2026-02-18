# A2A Project - Multi-Agent Badminton Scheduling System

A sophisticated multi-agent system built with the Agent-to-Agent (A2A) protocol for coordinating badminton game scheduling across multiple participants. This project demonstrates distributed AI agent orchestration using Google ADK, LangChain, and CrewAI frameworks.

## 🎯 Overview

The A2A Project implements a decentralized scheduling system where multiple AI agents collaborate to organize badminton sessions. The system consists of:

- **ElonAgent**: Host/orchestration agent that coordinates scheduling across connected agents
- **JeffAgent**: Personal scheduling assistant for Jeff Bezos using LangGraph
- **MarkAgent**: Personal scheduling assistant for Mark using CrewAI

## ✨ Features

- **Multi-Agent Coordination**: Seamless communication between distributed agents using the A2A protocol
- **Intelligent Scheduling**: AI-powered availability checking and conflict resolution
- **Court Booking Integration**: Automated badminton court availability checking and reservation
- **Conversation Memory**: Context-aware conversations with persistent memory across sessions
- **Asynchronous Architecture**: High-performance async/await patterns for concurrent operations
- **Modular Design**: Independent agents that can be deployed and scaled separately

## 🏗️ Architecture

```
┌─────────────────┐
│   ElonAgent     │  ← Host/Orchestrator (Google ADK)
│  (Coordinator)  │
└────────┬────────┘
         │ A2A Protocol
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼────┐
│Jeff   │ │ Mark  │  ← Remote Agents
│Agent  │ │ Agent │
│(Lang  │ │(Crew  │
│Graph) │ │ AI)   │
└───────┘ └───────┘
```

### Agent Responsibilities

- **ElonAgent**: Discovers remote agents, coordinates availability collection, determines compatible time slots, verifies court availability, and handles booking
- **JeffAgent**: Manages Jeff Bezos's schedule, responds to availability queries using LangGraph with memory checkpointing
- **MarkAgent**: Manages Mark's schedule, processes scheduling queries using CrewAI with Gemini LLM

## 🚀 Getting Started

### Prerequisites

- Python >= 3.13
- [uv](https://github.com/astral-sh/uv) package manager (recommended) or pip
- API keys for:
  - Groq API (for LLM access)
  - Google API (if using Gemini)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd a2a-project
   ```

2. **Install dependencies**

   Using uv (recommended):
   ```bash
   uv sync
   ```

   Or using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**

   Create a `.env` file in the project root:
   ```env
   Groq_API_KEY=your_groq_api_key_here
   ```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `Groq_API_KEY` | API key for Groq LLM services | Yes |

### Agent Endpoints

By default, the agents run on:
- **JeffAgent**: `http://localhost:10004`
- **MarkAgent**: `http://localhost:10005`

These can be configured in `elon_agent/agent.py`:

```python
friend_urls = [
    "http://localhost:10004",  # JeffAgent
    "http://localhost:10005"   # MarkAgent
]
```

## 📖 Usage

### Running Individual Agents

**JeffAgent:**
```bash
cd jeff_agent
python -m jeff_agent
```

**MarkAgent:**
```bash
cd mark_agent
python -m mark_agent
```

**ElonAgent (Host):**
```bash
cd elon_agent
python agent.py
```

### Example Interaction Flow

1. Start the remote agents (JeffAgent and MarkAgent) on their respective ports
2. Start the ElonAgent orchestrator
3. ElonAgent discovers and connects to remote agents
4. Send scheduling requests through ElonAgent
5. ElonAgent coordinates with remote agents to find compatible time slots
6. System checks court availability and books if possible

## 📁 Project Structure

```
a2a-project/
├── elon_agent/           # Host/orchestration agent
│   ├── agent.py          # Main orchestrator implementation
│   └── tools.py          # Court booking and availability tools
├── jeff_agent/           # Jeff's scheduling agent
│   ├── agent.py          # LangGraph-based agent
│   ├── agent_executor.py # A2A protocol executor
│   ├── tools.py          # Availability checking tools
│   └── __main__.py       # Entry point
├── mark_agent/           # Mark's scheduling agent
│   ├── agent.py          # CrewAI-based agent
│   ├── agent_executor.py # A2A protocol executor
│   ├── tools.py          # Availability checking tools
│   └── __main__.py       # Entry point
├── pyproject.toml        # Project dependencies and metadata
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (create this)
└── README.md             # This file
```

## 🛠️ Technology Stack

- **A2A SDK** (>=0.3.11): Agent-to-Agent communication protocol
- **Google ADK** (>=1.25.0): Agent development kit for orchestration
- **LangChain** (>=1.2.10): LLM application framework
- **LangGraph** (>=0.2.0): Stateful agent workflows
- **CrewAI** (>=1.4.1): Multi-agent orchestration framework
- **LiteLLM** (>=1.81.13): Unified LLM interface
- **Groq**: High-performance LLM inference
- **Uvicorn** (>=0.30.0): ASGI web server
- **httpx** (>=0.27.0): Async HTTP client

## 🔧 Development

### Code Style

The project follows Python best practices with:
- Type hints for improved code clarity
- Comprehensive docstrings
- Async/await patterns for concurrent operations
- Modular architecture with clear separation of concerns

### Adding New Agents

To add a new scheduling agent:

1. Create a new agent directory (e.g., `new_agent/`)
2. Implement an agent class with scheduling capabilities
3. Create an `AgentExecutor` that extends `a2a.server.agent_execution.AgentExecutor`
4. Register the agent endpoint in ElonAgent's `friend_urls`
5. Ensure the agent exposes an A2A-compliant interface

## 📝 License

[Add your license information here]

## 🤝 Contributing

[Add contribution guidelines here]

## 📧 Support

[Add support/contact information here]

---

**Note**: This project is a demonstration of multi-agent systems using the A2A protocol. Ensure all API keys are kept secure and never committed to version control.
