# Messi Agent - Football Scheduling Assistant

A conversational AI agent built with CrewAI and the A2A (Agent-to-Agent) protocol that helps manage Messi's football scheduling. The agent uses Google's Gemini AI through CrewAI's framework to intelligently answer availability questions using a task-based execution model.

## Overview

Messi Agent is a specialized scheduling assistant that:
- Answers questions about Messi's availability for football games
- Uses CrewAI's agent framework for task execution
- Integrates with Google's Gemini 2.5 Flash model for intelligent responses
- Exposes an A2A-compliant API for agent-to-agent communication
- Employs a sequential task processing approach with dedicated tools

## Features

- **CrewAI Framework**: Leverages CrewAI's agent, task, and crew architecture
- **Calendar Checker Tool**: Custom tool to query Messi's availability
- **Task-Based Execution**: Uses CrewAI's Task and Crew patterns for structured responses
- **A2A Protocol Compliant**: Fully compatible with Agent-to-Agent communication standards
- **RESTful API**: Exposes standard endpoints including agent card and task management
- **Async Architecture**: Built with async/await for efficient concurrent operations
- **Sequential Processing**: Organized task handling through CrewAI's Process.sequential

## Architecture

The agent is built using several key components:

### Core Components

1. **MessiAgent** (`agent.py`)
   - Implements the core agent logic using CrewAI's Agent class
   - Integrates Google Gemini 2.5 Flash via CrewAI's LLM wrapper
   - Configured as a "Scheduling Assistant" with specific role and goals
   - Uses CrewAI's Crew and Task for structured execution

2. **MessiAgentExecutor** (`agent_executor.py`)
   - Implements the A2A `AgentExecutor` interface
   - Handles request context and event queuing
   - Manages task lifecycle (submit → start → complete)
   - Formats responses as A2A-compliant artifacts

3. **Tools** (`tools.py`)
   - `AvailabilityTool`: A CrewAI BaseTool wrapper for checking schedules
   - `get_availability`: Core function that checks Messi's calendar for specific dates
   - Returns structured responses with availability information

4. **Server** (`__main__.py`)
   - Configures the A2A agent card with skills and capabilities
   - Sets up HTTP endpoints using Starlette
   - Serves the agent on localhost:10005

## Installation

### Prerequisites

- Python 3.13+
- Virtual environment (recommended)
- Google API key for Gemini

### Setup

1. **Clone the repository and navigate to the Messi agent directory**:
   ```bash
   cd messi_agent
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**:
   ```bash
   pip install -r ../requirements.txt
   ```

4. **Configure environment variables**:
   Create a `.env` file in the `messi_agent` directory:
   ```env
   GEMINI_API_KEY=your_google_api_key_here
   ```

   **Note**: This agent uses `GEMINI_API_KEY` (not `GOOGLE_API_KEY`)

## Configuration

### Agent Configuration

The agent is configured with the following parameters in `agent.py`:

- **Framework**: CrewAI
- **Model**: `gemini/gemini-2.5-flash` (via CrewAI LLM wrapper)
- **Role**: Scheduling Assistant
- **Goal**: Answer questions about Messi's availability
- **Tools**: `[AvailabilityTool]`
- **Process**: Sequential task execution

### Server Configuration

Default server settings in `__main__.py`:
- **Host**: `localhost`
- **Port**: `10005`
- **Agent Name**: Messi's Agent
- **Version**: 1.0.0

## Usage

### Starting the Agent

Run the agent server:

```bash
python __main__.py
```

Or use the module form:

```bash
python -m messi_agent
```

The server will start on `http://localhost:10005`

### Testing the Agent Card

Check the agent's capabilities:

```bash
curl http://localhost:10005/.well-known/agent-card.json
```

### Example Interactions

**Query 1**: Check availability for a specific date
```
User: "Is Messi available on November 10th, 2025?"
Agent: "On 2025-11-10, Jeff is Available from 11:00 AM to 03:00 PM."
```

**Query 2**: Check an unavailable date
```
User: "Can Messi play on November 9th?"
Agent: "On 2025-11-09, Jeff is Busy all day."
```

**Query 3**: Check full day availability
```
User: "What about November 13th?"
Agent: "On 2025-11-13, Jeff is Available all day."
```

## API Endpoints

### Agent Card
**GET** `/.well-known/agent-card.json`

Returns agent metadata including:
- Agent name and description
- Supported skills
- Input/output modes
- Version information

### Task Management
**POST** `/tasks`

Creates a new task for the agent to process.

**GET** `/tasks/{task_id}`

Retrieves task status and results.

**POST** `/tasks/{task_id}/events`

Streams task execution events.

## Development

### Project Structure

```
messi_agent/
├── __init__.py
├── __main__.py          # Server entry point
├── agent.py             # Core agent implementation (CrewAI)
├── agent_executor.py    # A2A executor wrapper
├── tools.py             # Calendar checking tool
├── main.py              # Alternative entry point
└── readme.md            # This file
```

### Key Technologies

- **CrewAI**: Agent framework for task-based execution
- **Google Gemini**: Large language model for natural language understanding
- **A2A SDK**: Agent-to-Agent protocol implementation
- **Starlette**: ASGI web framework
- **Uvicorn**: ASGI server

### CrewAI vs LangChain

This agent uses **CrewAI** instead of LangChain (used by KDB Agent):

| Feature | CrewAI (Messi Agent) | LangChain (KDB Agent) |
|---------|---------------------|----------------------|
| Framework | Task-based with Crew | Graph-based with LangGraph |
| Memory | Task-level | Thread-based checkpointing |
| Execution | Sequential process | React agent loop |
| Tool Pattern | BaseTool class | @tool decorator |
| Configuration | Role/Goal/Backstory | System prompt |

### Extending the Agent

#### Adding New Tools

1. Define your tool in `tools.py`:
   ```python
   from crewai.tools import BaseTool

   class NewTool(BaseTool):
       name: str = "Tool Name"
       description: str = "Tool description"

       def _run(self, param: str) -> str:
           # Implementation
           return "result"
   ```

2. Add to the agent's tools list in `agent.py`:
   ```python
   tools=[AvailabilityTool(), NewTool()]
   ```

#### Modifying Agent Behavior

Edit the agent configuration in `agent.py`:
```python
self.agent = Agent(
    role="Your custom role",
    goal="Your custom goal",
    backstory="Your custom backstory",
    tools=[AvailabilityTool()],
    llm=self.llm,
)
```

#### Changing the Model

Update the LLM configuration in `agent.py`:
```python
self.llm = LLM(
    model="gemini/gemini-2.0-pro",
    api_key=self.api_key,
)
```

#### Changing Process Type

Modify the Crew process in `agent.py`:
```python
crew = Crew(
    agents=[self.agent],
    tasks=[task],
    process=Process.hierarchical,  # or Process.sequential
)
```

## Available Dates

The agent currently has availability data for:
- **2025-11-09**: Busy all day
- **2025-11-10**: Available from 11:00 AM to 03:00 PM
- **2025-11-11**: Available from 11:00 AM to 03:00 PM
- **2025-11-13**: Available all day
- **2025-11-14**: Busy all day

## Comparison with KDB Agent

The project contains two similar agents showcasing different frameworks:

| Aspect | Messi Agent (CrewAI) | KDB Agent (LangChain) |
|--------|---------------------|---------------------|
| Port | 10005 | 10004 |
| Framework | CrewAI | LangChain + LangGraph |
| API Key Env | GEMINI_API_KEY | GOOGLE_API_KEY |
| Memory | Task-scoped | Thread-based persistent |
| Architecture | Role-based agents | React agent pattern |
| Best For | Task-oriented workflows | Conversational memory |

## Troubleshooting

### Import Errors

If you encounter module import errors:
```bash
pip install crewai langchain-google-genai a2a-sdk
```

### API Key Issues

Ensure your `.env` file contains `GEMINI_API_KEY` (not `GOOGLE_API_KEY`):
```env
GEMINI_API_KEY=your_api_key_here
```

### CrewAI Model Configuration

If you encounter model errors, ensure the model name includes the provider:
```python
model="gemini/gemini-2.5-flash"  # Correct
model="gemini-2.5-flash"          # Incorrect
```

### Port Already in Use

Change the port in `__main__.py`:
```python
def main(host="localhost", port=YOUR_PORT):
```

### Task Execution Errors

If tasks fail, check the task description and expected output format:
```python
task = Task(
    description="Clear, specific instruction",
    expected_output="Clear description of expected result",
    agent=self.agent
)
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | Yes | Google Gemini API key for LLM access |

## License

This project is part of the A2A Protocol Multi-Agent GenAI Application (L3).

## Contributing

1. Follow the existing code structure
2. Maintain async/await patterns
3. Update this README with any new features
4. Test agent responses before committing
5. Follow CrewAI best practices for agent design

## Resources

- [CrewAI Documentation](https://docs.crewai.com/)
- [A2A Protocol Specification](https://a2a.dev/)
- [Google Gemini API](https://ai.google.dev/)

## Contact

For questions or issues, please refer to the main project documentation.