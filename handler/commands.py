from .api import fetch, create_response, Embed
import json
import os
from .db import col

__all__ = ["SlashCommands"]


class SlashCommands:
    def process(self, data: dict):
        return getattr(SlashCommands, data["name"]+"_command")(data)

    @staticmethod
    def ping_command(data: dict):
        return create_response({
            "content": "Pong!"
        })
    
    @staticmethod
    def help_command(data: dict):
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

    @staticmethod
    def about_command(data: dict):
        return create_response({
            "content": "Thanks for ask about me :>!"
        })

    @staticmethod
    def invite_command(data: dict):
        client_id = os.environ.get("CLIENT_APPLICATION_ID")
        return create_response({
            "content": f"https://discord.com/oauth2/authorize?client_id={client_id}&permissions=59456&scope=applications.commands%20bot"
        })
    