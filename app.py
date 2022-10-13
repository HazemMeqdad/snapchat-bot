import random
from flask import Flask, request, jsonify
from discord_interactions import verify_key_decorator, InteractionType, InteractionResponseType
import argparse
import os
from handler.slash_commands import SlashCommands
import sys

app = Flask(__name__)
CLIENT_PUBLIC_KEY = os.getenv("CLIENT_PUBLIC_KEY")

@app.route("/")
def index():
    return "The bot is running now!"

@app.route("/interactions", methods=["POST"])
@verify_key_decorator(CLIENT_PUBLIC_KEY)
def interactions():
    data = request.json.get("data")
    if request.json["type"] == InteractionType.PING:
        return jsonify({"type": InteractionResponseType.PONG})
    elif request.json["type"] == InteractionType.APPLICATION_COMMAND:
        return jsonify(SlashCommands().process(data))
    elif request.json["type"] == InteractionType.MESSAGE_COMPONENT:
        ...
    elif request.json["type"] == InteractionType.APPLICATION_COMMAND_AUTOCOMPLETE:
        ...
    elif request.json["type"] == InteractionType.MODAL_SUBMIT:
        ...


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-u", "--update", help="Update bulk globle commands.", action="store_true", )
    parser.add_argument("-v", "--version", action="version", version="%(prog)s - Version 1.0")

    args = parser.parse_args()
    if not os.getenv("CLIENT_APPLICATION_ID"):
        print("CLIENT_APPLICATION_ID is not set.")
        sys.exit(1)
    if not os.getenv("CLIENT_BOT_TOKEN"):
        print("CLIENT_BOT_TOKEN is not set.")
        sys.exit(1)
    if not args.update:
        app.run("0.0.0.0", random.randint(1000, 10000), debug=True)
    else:
        from register_commands import update_global_commands
        update_global_commands(os.getenv("CLIENT_APPLICATION_ID"))
        print("Updated global commands.")
