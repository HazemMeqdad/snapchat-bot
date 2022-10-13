from handler.api import fetch
import json
import os

def update_global_commands(application_id: str):
    with open("data/commands.json", "r") as f:
        commands = json.load(f)
    fetch("PUT", f"/applications/{application_id}/commands", json=commands)

def update_guild_commands(guild_id: int):
    application_id = os.environ.get("CLIENT_APPLICATION_ID")
    with open("data/commands.json", "r") as f:
        commands = json.load(f)
    fetch("PUT", f"/applications/{application_id}/guilds/{guild_id}/commands", json=commands)

