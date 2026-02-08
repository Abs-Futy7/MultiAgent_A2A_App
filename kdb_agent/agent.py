from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.messages.ai import AIMessage
from tools import get_availability


# Step1: Agent & Tool


load_dotenv()

memory = MemorySaver()


class KDBAgent():

    SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]

    def __init__(self):
        
        self.model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
        self.tools = [get_availability] if get_availability else []
        self.system_prompt = ("You are KDB's scheduling assistant.\n"
                    "Your only job is to use the 'get_availability' tool "
                    "to answer questions about KDB's schedule for playing football.\n\n"
                    "If the question is unrelated to scheduling, politely say you can’t help.\n"
                )
        self.graph = create_agent(
            self.model,
            tools=self.tools,
            system_prompt=self.system_prompt,
            checkpointer=memory
        )

    async def get_response(self, query, context_id):
        inputs = {"messages": [("user", query)]}
        config = {"configurable": {"thread_id": context_id}}
        raw_response = self.graph.invoke(inputs, config)
        messages = raw_response.get("messages", [])
        ai_messages = [message.content for message in messages if isinstance(message, AIMessage)]
        
        if not ai_messages:
            return {"content": "No response"}
        
        # Handle both string content and list of content parts
        content = ai_messages[-1]
        if isinstance(content, list):
            # Extract text from content parts
            text_parts = [part.get("text", "") if isinstance(part, dict) else str(part) for part in content]
            response = " ".join(text_parts)
        else:
            response = str(content)
        
        return {"content": response}
    
#agent = KDBAgent()
#import asyncio
#response = asyncio.run(agent.get_response(query="Is KDB available on 8th Nov 2025? ", context_id=1234))
#print(response)