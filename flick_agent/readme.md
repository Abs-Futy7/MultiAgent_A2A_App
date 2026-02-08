# Flick Agent - Football Game Coordinator

A multi-agent coordinator built with Google ADK (Agent Development Kit) and the A2A (Agent-to-Agent) protocol that orchestrates football games with friends. The agent acts as a central host, coordinating with friend agents to find availability, book football fields, and organize games.

## Overview

Flick Agent is a host coordinator that:
- Connects to multiple friend agents via A2A protocol
- Coordinates football game scheduling across multiple participants
- Checks and books football field availability
- Uses Google's Gemini 2.5 Pro for intelligent orchestration
- Manages agent-to-agent communication seamlessly
- Provides an interactive web interface via ADK

## Features

- **Multi-Agent Coordination**: Communicates with multiple friend agents (Messi Agent, KDB Agent)
- **A2A Protocol Integration**: Full support for Agent-to-Agent communication standard
- **Football Field Management**: Check availability and book time slots
- **Intelligent Scheduling**: Finds common availability across multiple participants
- **Google ADK Integration**: Built on Google's Agent Development Kit
- **Interactive Web UI**: Access via ADK web interface for easy interaction
- **Async Architecture**: Handles concurrent agent communications efficiently

## Architecture

The agent is built using several key components:

### Core Components

1. **FlickAgent** (`flick/agent.py`)
   - Main coordinator agent using Google ADK's Agent class
   - Manages connections to remote friend agents
   - Integrates Google Gemini 2.5 Pro for orchestration logic
   - Handles agent discovery and card resolution
   - Coordinates scheduling workflow across agents

2. **RemoteAgentConnection** (`flick/agent.py`)
   - Represents individual connections to friend agents
   - Wraps A2AClient for HTTP-based agent communication
   - Manages message sending and response handling

3. **Tools** (`flick/tools.py`)
   - `list_field_availabilities(date)`: Lists available and booked time slots for a specific date
   - `book_football_field(date, start_time, end_time, reservation_name)`: Books a field for a reservation
   - In-memory field schedule management for demonstration

4. **Entry Points**
   - `agent.py`: ADK web interface entry point with `root_agent`
   - `flick/agent.py`: Core agent implementation with async setup

## Installation

```powershell
# Navigate to project root
cd E:\WebDev\A2A_Protocol\L3(Multi-Agent-GenAI-App)

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

## Configuration

### Environment Variables

Create a `.env` file in the project root with:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### Friend Agent URLs

Configure friend agents in `flick/agent.py`:

```python
friend_urls = ["http://localhost:10004", "http://localhost:10005"]
```

Default configuration:
- KDB Agent: `http://localhost:10004`
- Messi Agent: `http://localhost:10005`

## Usage

### Running with ADK Web Interface

```powershell
# From project root
cd E:\WebDev\A2A_Protocol\L3(Multi-Agent-GenAI-App)

# Start ADK web server
adk web
```

The web interface will start at `http://localhost:8000` and automatically discover the flick agent.

### Typical Workflow

1. **Start Friend Agents**: Ensure Messi Agent and KDB Agent are running on their respective ports
2. **Launch Flick Agent**: Start via ADK web interface
3. **Coordinate Game**: 
   - Ask friends for availability
   - Find common time slots
   - Check field availability
   - Book the field when confirmed

### Example Interactions

**Query 1: Check Friend Availability**
```
User: "Is Messi available tomorrow at 10 AM?"
Flick: [Contacts Messi Agent and returns availability status]
```

**Query 2: Find Common Time**
```
User: "When are both Messi and KDB available this week?"
Flick: [Contacts both agents and finds overlapping availability]
```

**Query 3: Book a Field**
```
User: "Book a field for November 11, 2025 at 11:00 AM"
Flick: [Checks field availability and makes reservation]
```

## Field Schedule

The agent maintains an in-memory field schedule with the following structure:

```python
FIELD_SCHEDULE = {
    "2025-11-10": {"08:00": "unknown", "09:00": "unknown", "10:00": "unknown"},
    "2025-11-11": {"08:00": "unknown", "09:00": "unknown", "10:00": "busy", "11:00": "available"},
    "2025-11-12": {"08:00": "unknown", "09:00": "unknown", "10:00": "unknown"},
}
```

Status values:
- `"unknown"`: Slot is available for booking
- `"available"`: Explicitly marked as available
- `"busy"`: Slot is already booked
- `[name]`: Slot booked by the named party

## Tools Reference

### list_field_availabilities

**Parameters:**
- `date` (str): Date in format "YYYY-MM-DD"

**Returns:**
```python
{
    "status": "success",
    "message": "Schedule for 2025-11-11.",
    "available_slots": ["08:00", "09:00"],
    "booked_slots": {"10:00": "busy", "11:00": "available"}
}
```

### book_football_field

**Parameters:**
- `date` (str): Date in format "YYYY-MM-DD"
- `start_time` (str): Start time in format "HH:MM"
- `end_time` (str): End time in format "HH:MM"
- `reservation_name` (str): Name for the reservation

**Returns:**
```python
{
    "status": "success",
    "message": "Booked 2025-11-11 at 11:00 for Team A."
}
```

### send_message

**Parameters:**
- `agent_name` (str): Name of the friend agent
- `task` (str): Message/task to send
- `tool_context` (ToolContext): ADK tool context

**Returns:** A2A SendMessageResponse with agent's reply

## Agent Card

The Flick Agent exposes an A2A agent card with:

**Skills:**
- Coordinate football games
- Check friend availability
- Book football fields
- Find common scheduling times

**Communication:**
- Protocol: A2A (Agent-to-Agent)
- Message format: JSON with structured parts
- Transport: HTTP/HTTPS

## API Rate Limits

### Free Tier (Gemini 2.5 Pro)
- 5 requests per minute
- Consider switching to gemini-1.5-flash (15 requests per minute) for development

### Recommendations
- Enable billing for production use (1500 requests/min)
- Implement exponential backoff for rate limit errors
- Add request queuing for better reliability

## Troubleshooting

### "No root_agent found"
**Solution:** Run `adk web` from the project root directory, not from inside the flick_agent folder.

### "429 RESOURCE_EXHAUSTED"
**Solution:** 
1. Wait 60 seconds for rate limit reset
2. Switch to gemini-1.5-flash model
3. Enable billing in Google Cloud Console

### Friend Agents Not Responding
**Solution:** 
1. Verify friend agents are running on configured ports
2. Check network connectivity to localhost
3. Review friend agent logs for errors

### Module Import Errors
**Solution:**
1. Ensure virtual environment is activated
2. Install all dependencies: `pip install -r requirements.txt`
3. Verify Python version compatibility

## Dependencies

- `google-adk`: Google Agent Development Kit
- `httpx`: Async HTTP client for A2A communication
- `python-dotenv`: Environment variable management
- `nest-asyncio`: Nested async event loop support
- `a2a-sdk`: Agent-to-Agent protocol SDK

## Project Structure

```
flick_agent/
├── agent.py                 # ADK entry point
├── readme.md               # This file
└── flick/
    ├── __init__.py         # Module initialization
    ├── agent.py            # Core FlickAgent implementation
    └── tools.py            # Field booking and availability tools
```

## Related Agents

- **KDB Agent** (`kdb_agent/`): LangChain-based scheduling assistant for KDB
- **Messi Agent** (`messi_agent/`): CrewAI-based scheduling assistant for Messi

## Contributing

When extending Flick Agent:
1. Maintain A2A protocol compatibility
2. Add comprehensive error handling for agent communications
3. Update agent card when adding new skills
4. Document new tools in this README
5. Test with all friend agents before deployment

## License

This is a demonstration project for multi-agent coordination using the A2A protocol.

## Support

For issues related to:
- **ADK**: [Google ADK Documentation](https://google.github.io/adk-docs/)
- **A2A Protocol**: Check A2A SDK documentation
- **Rate Limits**: [Gemini API Rate Limits](https://ai.google.dev/gemini-api/docs/rate-limits)
- **Agent Issues**: Review agent logs and verify friend agent connectivity

---

**Version:** 1.0.0  
**Last Updated:** February 8, 2026  
**Model:** Google Gemini 2.5 Pro