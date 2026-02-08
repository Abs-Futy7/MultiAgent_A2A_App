# Multi-Agent Football Game Coordinator

A sophisticated multi-agent system built on the A2A (Agent-to-Agent) protocol that demonstrates distributed agent coordination for scheduling football games. The system consists of three specialized AI agents that communicate using standardized protocols to find availability, coordinate schedules, and book football fields.

## 🎯 Overview

This project showcases a practical implementation of multi-agent systems where:
- **Flick Agent** (Host/Coordinator) orchestrates the entire scheduling workflow using Google ADK
- **KDB Agent** manages KDB's availability using LangChain with conversation memory
- **Messi Agent** manages Messi's availability using CrewAI with task-based execution

All agents communicate via the **A2A Protocol**, enabling standardized agent-to-agent interactions over HTTP.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Flick Agent (Host)                      │
│              Google ADK + Gemini 2.5 Pro                    │
│          - Orchestrates game coordination                   │
│          - Manages agent-to-agent communication             │
│          - Books football fields                            │
└────────────┬──────────────────────────────┬─────────────────┘
             │                              │
      A2A Protocol (HTTP)          A2A Protocol (HTTP)
             │                              │
   ┌─────────▼──────────┐        ┌─────────▼──────────┐
   │   KDB Agent        │        │  Messi Agent       │
   │ LangChain + Memory │        │ CrewAI + Tasks     │
   │ :10004             │        │ :10005             │
   └────────────────────┘        └────────────────────┘
```

## 🤖 Agents

### 1. Flick Agent (Coordinator)
**Technology:** Google ADK (Agent Development Kit)  
**Model:** Google Gemini 2.5 Pro  
**Port:** Managed by ADK web (default: 8000)  
**Role:** Central coordinator

**Capabilities:**
- Connects to multiple friend agents via A2A protocol
- Finds common availability across participants
- Checks football field availability
- Books fields when schedule is confirmed
- Provides interactive web UI via ADK

**Tools:**
- `send_message(agent_name, task)` - Communicate with friend agents
- `list_field_availabilities(date)` - Check field schedule
- `book_football_field(date, time, name)` - Reserve a field

[📖 Full Documentation](flick_agent/readme.md)

### 2. KDB Agent (Scheduling Assistant)
**Technology:** LangChain + LangGraph  
**Model:** Google Gemini 2.5 Flash  
**Port:** 10004  
**Role:** KDB's personal scheduling assistant

**Capabilities:**
- Manages KDB's calendar and availability
- Maintains conversation context with memory checkpointing
- Natural language understanding for scheduling queries
- A2A-compliant API for external communication

**Tools:**
- `get_availability(date)` - Check KDB's schedule for specific dates

[📖 Full Documentation](kdb_agent/readme.md)

### 3. Messi Agent (Scheduling Assistant)
**Technology:** CrewAI Framework  
**Model:** Google Gemini 2.5 Flash  
**Port:** 10005  
**Role:** Messi's personal scheduling assistant

**Capabilities:**
- Manages Messi's calendar and availability
- Task-based execution with CrewAI's sequential processing
- Structured responses using Agent/Task/Crew patterns
- A2A-compliant API for external communication

**Tools:**
- `AvailabilityTool` - Check Messi's schedule with CrewAI wrapper

[📖 Full Documentation](messi_agent/readme.md)

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Google Gemini API Key
- Virtual environment (recommended)

### Installation

```powershell
# Clone/Navigate to project
cd E:\WebDev\A2A_Protocol\L3(Multi-Agent-GenAI-App)

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### Running the System

**Step 1: Start Friend Agents**

```powershell
# Terminal 1 - Start KDB Agent
cd kdb_agent
python __main__.py
# Server running on http://localhost:10004

# Terminal 2 - Start Messi Agent
cd messi_agent
python __main__.py
# Server running on http://localhost:10005
```

**Step 2: Start Flick Agent (Coordinator)**

```powershell
# Terminal 3 - Start Flick Agent with ADK web
cd E:\WebDev\A2A_Protocol\L3(Multi-Agent-GenAI-App)
adk web
# Web UI available at http://localhost:8000
```

**Step 3: Interact via ADK Web UI**

Open your browser to `http://localhost:8000` and start coordinating football games!

## 📋 Example Workflow

### Scenario: Organizing a Football Game

1. **User:** "When are Messi and KDB both available this week?"
   - Flick Agent contacts both friend agents
   - Collects availability from each
   - Returns overlapping time slots

2. **User:** "Check if the field is available on November 11 at 11 AM"
   - Flick Agent queries field schedule
   - Returns availability status

3. **User:** "Book the field for that time"
   - Flick Agent reserves the field
   - Confirms booking with timestamp

### Sample Interactions

```
> "Is Messi available tomorrow at 10 AM?"
↳ Flick sends message to Messi Agent
↳ Returns: "Yes, Messi is available on November 9, 2025 at 10:00 AM"

> "What about KDB on the same day?"
↳ Flick sends message to KDB Agent  
↳ Returns: "KDB is available on November 9, 2025 at 10:00 AM"

> "Great! Book a field for both of them at 10 AM on November 9"
↳ Flick books field
↳ Returns: "✅ Booked 2025-11-09 at 10:00 for Football Game"
```

## 🔧 Technology Stack

### Frameworks
- **Google ADK** - Agent Development Kit for orchestration
- **LangChain** - Agent framework with memory and tools
- **CrewAI** - Multi-agent framework with task management
- **LangGraph** - Graph-based agent workflows

### AI Models
- **Gemini 2.5 Pro** - Advanced reasoning for coordination (Flick)
- **Gemini 2.5 Flash** - Fast responses for scheduling (KDB, Messi)

### Communication
- **A2A Protocol** - Agent-to-Agent communication standard
- **A2A SDK** - Python implementation of A2A protocol
- **HTTP/REST** - Transport layer for agent messages

### Infrastructure
- **Starlette** - Async web framework for agent servers
- **Uvicorn** - ASGI server for production deployment
- **SSE-Starlette** - Server-Sent Events for real-time updates
- **httpx** - Async HTTP client for inter-agent communication

## 📁 Project Structure

```
L3(Multi-Agent-GenAI-App)/
├── readme.md                    # This file
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (create this)
├── workflow.drawio             # Architecture diagram
│
├── flick_agent/                # Host/Coordinator Agent
│   ├── agent.py                # ADK entry point
│   ├── readme.md               # Flick agent documentation
│   └── flick/
│       ├── __init__.py
│       ├── agent.py            # Core FlickAgent implementation
│       └── tools.py            # Field booking tools
│
├── kdb_agent/                  # KDB Scheduling Agent
│   ├── __main__.py             # Server entry point
│   ├── agent.py                # LangChain agent implementation
│   ├── agent_executor.py       # A2A executor wrapper
│   ├── tools.py                # Availability tools
│   ├── main.py                 # Alternative entry point
│   └── readme.md               # KDB agent documentation
│
└── messi_agent/                # Messi Scheduling Agent
    ├── __main__.py             # Server entry point
    ├── agent.py                # CrewAI agent implementation
    ├── agent_executor.py       # A2A executor wrapper
    ├── tools.py                # Availability tools
    ├── main.py                 # Alternative entry point
    └── readme.md               # Messi agent documentation
```

## 🔒 A2A Protocol

All agents implement the A2A (Agent-to-Agent) protocol, which provides:

### Standard Endpoints
- `GET /.well-known/agent.json` - Agent card (capabilities, metadata)
- `POST /tasks` - Submit new tasks
- `GET /tasks/{taskId}` - Get task status
- `POST /tasks/{taskId}/start` - Start task execution
- `GET /tasks/{taskId}/steps` - Stream task progress

### Agent Cards
Each agent exposes a card with:
- **name** - Agent identifier
- **description** - Agent purpose
- **url** - Agent endpoint
- **skills** - List of capabilities
- **communication** - Protocol details

### Message Format
```json
{
  "message": {
    "role": "user",
    "parts": [{"type": "text", "text": "query"}],
    "messageId": "uuid"
  }
}
```

## 🛠️ Development

### Adding a New Agent

1. **Create agent directory**
```powershell
mkdir new_agent
cd new_agent
```

2. **Implement agent with chosen framework** (LangChain, CrewAI, or ADK)

3. **Create A2A executor** implementing `AgentExecutor` interface

4. **Set up HTTP server** with Starlette/Uvicorn

5. **Add agent card** at `/.well-known/agent.json`

6. **Update Flick agent** to include new friend URL

### Testing Agent Communication

```python
# Test A2A connection
import httpx
import asyncio

async def test_agent():
    async with httpx.AsyncClient() as client:
        # Get agent card
        response = await client.get("http://localhost:10004/.well-known/agent.json")
        print(response.json())
        
        # Submit task
        response = await client.post(
            "http://localhost:10004/tasks",
            json={
                "message": {
                    "role": "user",
                    "parts": [{"type": "text", "text": "Are you available tomorrow?"}]
                }
            }
        )
        print(response.json())

asyncio.run(test_agent())
```

## ⚠️ Common Issues

### 1. Rate Limiting (429 Error)
**Problem:** Gemini API free tier limits exceeded

**Solutions:**
- Wait 60 seconds between requests
- Switch to `gemini-1.5-flash` (15 req/min vs 5)
- Enable billing for production (1500 req/min)

### 2. Agent Not Found
**Problem:** `adk web` can't find agents

**Solutions:**
- Run from project root, not inside agent folders
- Ensure `root_agent` is defined at module level
- Check agent directory structure

### 3. Connection Refused
**Problem:** Friend agents not responding

**Solutions:**
- Verify agents are running on correct ports (10004, 10005)
- Check firewall/antivirus settings
- Confirm localhost connectivity

### 4. Import Errors
**Problem:** Missing dependencies

**Solutions:**
- Activate virtual environment: `.\.venv\Scripts\Activate.ps1`
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python version (3.9+)

## 📊 Performance Considerations

### Request Rates
- **Free Tier:** 5-15 requests/minute depending on model
- **Paid Tier:** 1500 requests/minute
- **Recommendation:** Implement request queuing for production

### Latency
- **Single Agent Query:** ~1-3 seconds
- **Multi-Agent Coordination:** ~3-6 seconds
- **Field Booking:** <100ms (in-memory)

### Scalability
- Current: In-memory storage (demo purposes)
- Production: Replace with persistent database (PostgreSQL, Redis)
- Horizontal: Deploy agents across multiple servers

## 🧪 Testing

### Unit Tests
```powershell
# Test individual agent
cd kdb_agent
python -m pytest tests/

# Test tools
python -c "from tools import get_availability; print(get_availability('2025-11-10'))"
```

### Integration Tests
```powershell
# Test A2A communication
python test_a2a_protocol.py

# Test multi-agent workflow
python test_coordination.py
```

## 🔐 Security Considerations

### API Keys
- Never commit `.env` files to version control
- Use environment variables for sensitive data
- Rotate API keys regularly

### Network Security
- Currently running on localhost (development)
- For production: Use HTTPS/TLS
- Implement authentication for agent endpoints

### Data Privacy
- Agent conversations are in-memory (cleared on restart)
- For production: Implement proper data retention policies
- Comply with privacy regulations (GDPR, etc.)

## 🚦 Roadmap

### Phase 1: Current (✅ Complete)
- [x] Basic multi-agent coordination
- [x] A2A protocol implementation
- [x] Field booking system
- [x] Web UI via ADK

### Phase 2: Enhancement
- [ ] Persistent storage (database integration)
- [ ] User authentication and authorization
- [ ] Extended calendar integration (Google Calendar, Outlook)
- [ ] Email/SMS notifications
- [ ] Payment integration for field bookings

### Phase 3: Advanced
- [ ] Machine learning for optimal scheduling
- [ ] Weather-based recommendations
- [ ] Team formation and player matching
- [ ] Multi-location field management
- [ ] Mobile app interface

## 📚 Resources

### Documentation
- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [LangChain Documentation](https://python.langchain.com/)
- [CrewAI Documentation](https://docs.crewai.com/)
- [A2A Protocol Specification](https://github.com/google/agent-to-agent-protocol)

### API References
- [Gemini API Docs](https://ai.google.dev/docs)
- [Gemini Rate Limits](https://ai.google.dev/gemini-api/docs/rate-limits)
- [Starlette Documentation](https://www.starlette.io/)

### Related Projects
- [LangGraph Examples](https://github.com/langchain-ai/langgraph)
- [CrewAI Examples](https://github.com/joaomdmoura/crewAI-examples)
- [Multi-Agent Systems Research](https://arxiv.org/list/cs.MA/recent)

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

1. **Agent Frameworks**: Add support for AutoGPT, Semantic Kernel, etc.
2. **Tools**: Implement additional scheduling/booking tools
3. **Testing**: Expand test coverage
4. **Documentation**: Add more examples and tutorials
5. **UI/UX**: Enhance web interface with React/Vue

## 📄 License

This is a demonstration project for educational purposes showcasing multi-agent coordination using the A2A protocol.

## 💡 Use Cases

This architecture can be adapted for:
- **Meeting Coordination** - Schedule meetings across organizations
- **Resource Booking** - Conference rooms, equipment, vehicles
- **Event Planning** - Coordinate multi-party events
- **Supply Chain** - Agent-based logistics coordination
- **Healthcare** - Patient scheduling across specialists
- **Education** - Course scheduling and resource allocation

## 👥 Authors

Multi-Agent Football Game Coordinator  
Demonstrating A2A Protocol and Multi-Agent Systems

## 🙏 Acknowledgments

- Google ADK Team for the Agent Development Kit
- LangChain Community for agent frameworks
- CrewAI Team for task-based agent coordination
- A2A Protocol contributors for standardized communication

---

**Version:** 1.0.0  
**Last Updated:** February 8, 2026  
**Status:** Development/Demo  

For detailed information about individual agents, see their respective README files in their directories.