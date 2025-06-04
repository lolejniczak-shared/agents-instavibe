from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from planner_agent_executor import PlannerAgentExecutor
import os

from dotenv import load_dotenv


load_dotenv()

##logging.basicConfig(level=logging.INFO)
##logger = logging.getLogger(__name__)

A2A_HOST = os.environ.get("A2A_HOST")
A2A_PORT = int(os.environ.get("A2A_PORT"))
A2A_PUBLIC_URL=os.environ.get("A2A_PUBLIC_URL")
 

def main():
    if A2A_PUBLIC_URL:
        PUBLIC_URL = A2A_PUBLIC_URL
        print(f"PUBLIC_URL is set from the .env file: {PUBLIC_URL}")
    else:
        PUBLIC_URL = f"http://{A2A_HOST}:{A2A_PORT}"
    
    capabilities = AgentCapabilities(streaming=True)

    skill = AgentSkill(
                id="night_out_planner",
                name="Night out planner",
                description="""
                This agent generates multiple fun plan suggestions tailored to your specified location, dates, and interests,
                all designed for a moderate budget. It delivers detailed itineraries,
                including precise venue information (name, latitude, longitude, and description), in a structured JSON format.
                """,
                tags=["instavibe"],
                examples=["What about Bostona MA this weekend?"],
            )
    agent_card = AgentCard(
                name="NightOut Planner Agent",
                description="""
                This agent generates multiple fun plan suggestions tailored to your specified location, dates, and interests,
                all designed for a moderate budget. It delivers detailed itineraries,
                including precise venue information (name, latitude, longitude, and description), in a structured JSON format.
                """,
                url=f"{PUBLIC_URL}",
                version="1.0.0",
                defaultInputModes=['text'],
                defaultOutputModes=['text'],
                capabilities=capabilities,
                skills=[skill],
            )

    request_handler = DefaultRequestHandler(
            agent_executor=PlannerAgentExecutor(),
            task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(
            agent_card=agent_card, 
            http_handler=request_handler
    )
    host = A2A_HOST
    port = A2A_PORT
    import uvicorn
    print(f"Starting Uvicorn server on {host}:{port}")
    uvicorn.run(server.build(), host=host, port=port)

if __name__ == '__main__':
    main()
