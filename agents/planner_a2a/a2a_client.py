from a2a.client import A2AClient
from typing import Any
import httpx
from uuid import uuid4
from a2a.types import (
    SendMessageRequest,
    MessageSendParams,
    SendStreamingMessageRequest,
)


async def main() -> None:
    async with httpx.AsyncClient() as httpx_client:
        client = await A2AClient.get_client_from_agent_card_url(
            httpx_client, base_url = 'https://planner-agent-680248386202.us-central1.run.app'
            ##, agent_card_path='/.well-known/agent.json'
        )
        send_message_payload: dict[str, Any] = {
            'message': {
                'role': 'user',
                'parts': [
                    {
                        'kind': 'text', 
                        'text': 'Plan something for tomorrow in warsaw. I like live music'
                    }
                ],
                'messageId': "foo2",
            },
        }
        request = SendMessageRequest(
            params=MessageSendParams(**send_message_payload)
        )

        response = await client.send_message(request)
        print(response.model_dump(mode='json', exclude_none=True))

        ##streaming_request = SendStreamingMessageRequest(
        ##    params=MessageSendParams(**send_message_payload)
        ##)

        ##stream_response = client.send_message_streaming(streaming_request)
        ##async for chunk in stream_response:
        ##    print(chunk.model_dump(mode='json', exclude_none=True))


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())