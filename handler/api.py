from requests import request
import typing as t
import os
from discord_interactions import InteractionResponseType
from dataclasses import dataclass, field

__all__ = ["fetch"]

BASE = "https://discord.com/api/v10"

def fetch(method: t.Literal["GET", "POST", "DELETE", "PUT"], route: str, **kwargs):
    return request(method, BASE + route, **kwargs, headers={"Authorization": f"Bot {os.environ.get('CLIENT_BOT_TOKEN')}"})

def create_response(data: t.Dict, response_type: int = InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE):
    return {"type": response_type, "data": data}


@dataclass
class Embed:
    """
    Embeds are a rich content format that allow you to create more visually rich messages.
    """
    title: t.Optional[str] = None
    type: str = "rich"
    description: t.Optional[str] = None
    url: t.Optional[str] = None
    timestamp: t.Optional[str] = None
    color: t.Optional[int] = None
    footer: dict = field(default_factory=dict)
    image: dict = field(default_factory=dict)
    thumbnail: dict = field(default_factory=dict)
    video: dict = field(default_factory=dict)
    provider: dict = field(default_factory=dict)
    auther: dict = field(default_factory=dict)
    fields: t.List[dict] = field(default_factory=list)

    def to_dict(self):
        return {
            "title": self.title,
            "type": self.type,
            "description": self.description,
            "url": self.url,
            "timestamp": self.timestamp,
            "color": self.color,
            "footer": self.footer,
            "image": self.image,
            "thumbnail": self.thumbnail,
            "video": self.video,
            "provider": self.provider,
            "auther": self.auther,
            "fields": self.fields
        }
