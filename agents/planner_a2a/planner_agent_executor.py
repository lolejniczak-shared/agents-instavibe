from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import (
    DataPart,
    Part,
    Task,
    TaskState,
    TextPart,
    UnsupportedOperationError,
)
from google.adk import Runner
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.sessions import InMemorySessionService
from google.genai import types

import agent
from a2a.utils.errors import ServerError
import logging 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PlannerAgentExecutor(AgentExecutor):
    """Agent executor that uses the ADK to answer questions."""

    def __init__(self):
        self.agent = None
        self.runner = None

    def _init_agent(self):
        self.agent = agent.root_agent
        self.runner = self.runner = Runner(
            app_name=self.agent.name,
            agent=self.agent,
            artifact_service=InMemoryArtifactService(),
            session_service=InMemorySessionService(),
            memory_service=InMemoryMemoryService(),
        )

    async def cancel(self, context: RequestContext, event_queue: EventQueue):
        raise ServerError(error=UnsupportedOperationError())

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        if self.agent is None:
            self._init_agent()
        logger.debug(f'Executing agent {self.agent.name}')

        query = context.get_user_input()

        updater = TaskUpdater(event_queue, context.task_id, context.context_id)

        if not context.current_task:
            updater.submit()

        updater.start_work()

        content = types.Content(role='user', parts=[types.Part(text=query)])
        session = await self.runner.session_service.get_session(
            app_name=self.runner.app_name,
            user_id='123',
            session_id=context.context_id,
        ) or await self.runner.session_service.create_session(
            app_name=self.runner.app_name,
            user_id='123',
            session_id=context.context_id,
        )

        async for event in self.runner.run_async(
            session_id=session.id, user_id='123', new_message=content
        ):
            logger.debug(f'Event from ADK {event}')
            if event.is_final_response():
                parts = event.content.parts
                text_parts = [
                    TextPart(text=part.text) for part in parts if part.text
                ]
                updater.add_artifact(
                    text_parts,
                    name='result',
                )
                updater.complete()
                break
            else:
                updater.update_status(
                    TaskState.working,
                    message=updater.new_text_message('Working...'),
                )
        else:
            ##logger.debug('Agent failed to complete')
            updater.update_status(
                TaskState.failed,
                message=updater.new_text_message('Failed to generate a response.'),
            )