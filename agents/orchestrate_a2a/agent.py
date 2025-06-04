from host_agent import HostAgent
import asyncio
import os # Import os to read environment variables
from dotenv import load_dotenv
from google.genai import types

load_dotenv()


REMOTE_AGENT_ADDRESSES_STR = os.getenv("REMOTE_AGENT_ADDRESSES", "")
print(f"Remote Agent Addresses String: {REMOTE_AGENT_ADDRESSES_STR}")
REMOTE_AGENT_ADDRESSES = [addr.strip() for addr in REMOTE_AGENT_ADDRESSES_STR.split(',') if addr.strip()]
print(f"Remote Agent Addresses: {REMOTE_AGENT_ADDRESSES}")

# --- Agent Initialization ---
async def setup_and_create_agent(): 
    # First, await the creation of the host_agent
    host_agent = await HostAgent.create(remote_agent_addresses=REMOTE_AGENT_ADDRESSES)
    print(host_agent.list_remote_agents()) 
    print("Host Agent created. Now creating the Root Agent...")
    final_agent = host_agent.create_agent()
    print("Root Agent created successfully.")
    return final_agent

# Create the actual ADK Agent instance
root_agent = asyncio.run(setup_and_create_agent())
print(root_agent.name)