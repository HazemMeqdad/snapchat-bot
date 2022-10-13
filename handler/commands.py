from .api import fetch, create_response, Embed
import json

__all__ = ["SlashCommands"]


class SlashCommands:
    def process(self, data: dict):
        return getattr(SlashCommands, data["name"])(data)

    @staticmethod
    def ping(data: dict):
        return create_response({
            "content": "Pong!"
        })
    
    @staticmethod
    def help(data: dict):
        embed = Embed(
            title="Help menu",
            description="This is a help menu for snapchat bot, share story notifications to discord\n\n",
            color=0x00FF00,
        )
        with open("data/commands.json") as f:
            commands = json.load(f)
        for command in commands:
            # sub slash commands
            if command.get("options"):
                for i in command["options"]:
                    if i["type"] != 1:
                        break
                    embed.fields.append({
                        "name": f"/{command['name']} {command['options'][0]['name']}",
                        "value": command["description"]
                    })

            # normal slash commands
            embed.description += f"**/{command['name']}** - {command['description']}\n"
            
        return create_response({
            "content": "Help!",
            "embeds": [embed.to_dict()]
        })

