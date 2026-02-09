import os
import asyncio
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.tools import load_mcp_tools
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langgraph.prebuilt import create_react_agent

load_dotenv()

# Define how to start the MCP server
server_params = StdioServerParameters(
    command="python", 
    args=["mcp_server.py"] # Ensure this matches your filename
)

async def main():
    # 1. Connect to the MCP Server
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # 2. Load MCP tools into LangChain format
            tools = await load_mcp_tools(session)
            
            # 3. Initialize Gemini
            llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
            
            # 4. Create the Agent
            agent = create_react_agent(llm, tools)
            
            # 5. Run a test
            query = "What is 156 multiplied by 82?"
            print(f"User: {query}")
            
            result = await agent.ainvoke({"messages": [("human", query)]})
            print(f"AI: {result['messages'][-1].content}")

if __name__ == "__main__":
    asyncio.run(main())