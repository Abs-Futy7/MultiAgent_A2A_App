# KDB Agent - Football Scheduling Assistant

A conversational AI agent built with LangChain and the A2A (Agent-to-Agent) protocol that helps manage KDB's football scheduling. The agent uses Google's Gemini AI to intelligently answer availability questions and maintain conversation context across sessions.

## Overview

KDB Agent is a specialized scheduling assistant that:
- Answers questions about KDB's availability for football games
- Uses natural language understanding to interpret scheduling queries
- Maintains conversation history with memory checkpointing
- Exposes an A2A-compliant API for agent-to-agent communication
- Integrates with Google's Gemini 2.5 Flash model for intelligent responses

## Features

- **Smart Scheduling Tool**: Query KDB's availability for specific dates
- **Conversational Memory**: Maintains context across multiple interactions using thread-based memory
- **A2A Protocol Compliant**: Fully compatible with Agent-to-Agent communication standards
- **Tool Integration**: Uses LangChain tools for availability checking
- **RESTful API**: Exposes standard endpoints including agent card and task management
- **Async Architecture**: Built with async/await for efficient concurrent operations

## Architecture

The agent is built using several key components:

### Core Components

1. **KDBAgent** (`agent.py`)
   - Implements the core agent logic using LangChain's `create_agent`
   - Integrates Google Gemini 2.5 Flash for language understanding
   - Uses MemorySaver for conversation persistence
   - Configured with a focused system prompt for scheduling tasks

2. **KDBAgentExecutor** (`agent_executor.py`)
   - Implements the A2A `AgentExecutor` interface
   - Handles request context and event queuing
   - Manages task lifecycle (submit → start → complete)
   - Formats responses as A2A-compliant artifacts

3. **Tools** (`tools.py`)
   - `get_availability`: Checks KDB's schedule for specific dates
   - Returns structured responses with availability information

4. **Server** (`__main__.py`)
   - Configures the A2A agent card with skills and capabilities
   - Sets up HTTP endpoints using Starlette
   - Serves the agent on localhost:10004

## Installation

### Prerequisites

- Python 3.13+
- Virtual environment (recommended)
- Google API key for Gemini

### Setup

1. **Clone the repository and navigate to the KDB agent directory**:
   ```bash
   cd kdb_agent
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
   Create a `.env` file in the `kdb_agent` directory:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## Configuration

### Agent Configuration

The agent is configured with the following parameters in `agent.py`:

- **Model**: `gemini-2.5-flash`
- **Tools**: `[get_availability]`
- **System Prompt**: Focused on football scheduling assistance
- **Memory**: Thread-based conversation memory with checkpointing

### Server Configuration

Default server settings in `__main__.py`:
- **Host**: `localhost`
- **Port**: `10004`
- **Agent Name**: KDB's Agent
- **Version**: 1.0.0

## Usage

### Starting the Agent

Run the agent server:

```bash
python __main__.py
```

Or use the module form:

```bash
python -m kdb_agent
```

The server will start on `http://localhost:10004`

### Testing the Agent Card

Check the agent's capabilities:

```bash
curl http://localhost:10004/.well-known/agent-card.json
```

### Example Interactions

**Query 1**: Check availability for a specific date
```
User: "Is KDB available on November 9th, 2025?"
Agent: "On 2025-11-09, Jeff is Available from 4:00 PM to 6:00 PM."
```

**Query 2**: Check an unavailable date
```
User: "Can KDB play on November 12th?"
Agent: "He is not available on 2025-11-12 as he's Busy all afternoon (1:00 PM – 5:00 PM)."
```

**Query 3**: Unrelated question
```
User: "What's the weather like?"
Agent: "I'm sorry, but I can only help with questions about KDB's schedule for playing football."
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
kdb_agent/
├── __init__.py
├── __main__.py          # Server entry point
├── agent.py             # Core agent implementation
├── agent_executor.py    # A2A executor wrapper
├── tools.py             # Scheduling tools
├── main.py              # Alternative entry point
└── readme.md            # This file
```

### Key Technologies

- **LangChain**: Agent framework and tool integration
- **LangGraph**: Agent execution graph and memory management
- **Google Gemini**: Large language model for natural language understanding
- **A2A SDK**: Agent-to-Agent protocol implementation
- **Starlette**: ASGI web framework
- **Uvicorn**: ASGI server

### Extending the Agent

#### Adding New Tools

1. Define your tool in `tools.py`:
   ```python
   def new_tool(param: str) -> dict:
       """Tool description for the LLM."""
       # Implementation
       return {"status": "completed", "message": "..."}
   ```

2. Add to the agent's tools list in `agent.py`:
   ```python
   self.tools = [get_availability, new_tool]
   ```

#### Modifying System Prompt

Edit the `system_prompt` in `agent.py` to change the agent's behavior:
```python
self.system_prompt = "Your new instructions here..."
```

#### Changing the Model

Update the model configuration in `agent.py`:
```python
self.model = ChatGoogleGenerativeAI(model="gemini-2.0-pro")
```

## Available Dates

The agent currently has availability data for:
- **2025-11-09**: Available from 4:00 PM to 6:00 PM
- **2025-11-10**: Available from 10:00 AM to 12:00 PM
- **2025-11-11**: Available from 11:00 AM to 12:00 PM
- **2025-11-12**: Busy all afternoon (1:00 PM – 5:00 PM)
- **2025-11-13**: Available all day

## Troubleshooting

### Import Errors

If you encounter module import errors:
```bash
pip install langchain langgraph langchain-google-genai
```

### API Key Issues

Ensure your `.env` file is in the correct directory and contains a valid Google API key.

### Port Already in Use

Change the port in `__main__.py`:
```python
def main(host="localhost", port=YOUR_PORT):
```

## License

This project is part of the A2A Protocol Multi-Agent GenAI Application (L3).

## Contributing

1. Follow the existing code structure
2. Maintain async/await patterns
3. Update this README with any new features
4. Test agent responses before committing

## Contact

For questions or issues, please refer to the main project documentation.