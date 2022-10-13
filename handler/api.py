from requests import request
import typing as t
import os
from discord_interactions import InteractionResponseType

__all__ = ["fetch"]

BASE = "https://discord.com/api/v10"

def fetch(method: t.Literal["GET", "POST", "DELETE", "PUT"], route: str, **kwargs):
    return request(method, BASE + route, **kwargs, headers={"Authorization": f"Bot {os.environ.get('CLIENT_BOT_TOKEN')}"})

def create_response(data: t.Dict, response_type: int = InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE):
    return {"type": response_type, "data": data}
