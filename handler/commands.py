from .api import fetch, create_response

__all__ = ["SlashCommands"]


class SlashCommands:
    def process(self, data: dict):
        return getattr(SlashCommands, data["name"])(data)

    @staticmethod
    def ping(data: dict):
        return create_response({
            "content": "Pong!"
        })

