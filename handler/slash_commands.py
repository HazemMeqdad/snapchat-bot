from pprint import pprint
from .api import fetch, create_response, Embed
import json
import os
from .db import col_guilds, col_users
from utlits.snapchat_user import get_user_data, get_user_story

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
    
    @staticmethod
    def setup_command(data: dict):
        if data.get("options"):
            if data["options"][0]["name"] == "user":
                SlashCommands.setup_user_command(data)

    @staticmethod
    def setup_user_command(data: dict):
        pprint(data)
        username = data["options"][0]["options"][0]["value"]
        channel = data["options"][1]["options"][1]["value"]
        message = data["options"][2]["options"][2]["value"] or "{username} has posted a new story!\n{url}"
        if "{url}" not in message:
            message += "\n{url}"

        # check if the guild can add this user to database
        guild = col_guilds.find_one({"guild_id": data["guild_id"]})
        if not guild:
            col_guilds.insert_one({
                "guild_id": data["guild_id"],
                "channels": [],
                "users_count": 1  # can add more for premium users only
            })
            guild = col_guilds.find_one({"guild_id": data["guild_id"]})
        if guild["users_count"] >= len(guild["channels"]):
            return create_response({
                "content": "You reached the maximum users limit, please upgrade to premium to add more users\n\n"
                            "You can upgrade to premium by donating **2.99$** per user to the bot owner"
            })

        # check if snapchat username exists on database
        username_exists = col_users.find_one({"username": username})
        if not username_exists:
            col_users.insert_one({
                "username": username,
                "channels": [],
            })
        col_users.update_one({"username": username}, {"$push": {"channels": {"channel_id": channel, "message": message}}})

        user = get_user_data(username)
        if not user:
            return create_response({
                "content": "This snapchat username doesn't exists"
            })
        fetch("POST", f"/channels/{channel}/messages", json={
            "content": "**Test message**\n\n" + message.format(username=username, url=f"https://www.snapchat.com/add/{username}")
        })
        return create_response({
            "content": f"[@{username}](https://www.snapchat.com/add/{username}) has been added to <#{channel}>, will send a message when they post a new story",
        })
