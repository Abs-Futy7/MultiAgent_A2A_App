"""
Flick Agent - ADK Entry Point
This file provides the root_agent for ADK web interface.
"""
import asyncio
from flick.agent import setup

# Create the agent instance for ADK web
# nest_asyncio is already applied in flick.agent module
root_agent = asyncio.run(setup())
