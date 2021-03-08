import logging
import os
from collections import defaultdict

from flask import Flask, abort, jsonify, request

from client.player import Player

NUM_PLAYERS = os.getenv("NUM_PLAYERS")
app = Flask(__name__)
player = Player()


@app.route("/hey/", methods=["post"])
def register_peer():
    data = request.get_json()

    if data is None or "address" not in data:
        abort(400, "Please specify the 'address' value")

    if len(player.peer_addresses) >= NUM_PLAYERS:
        abort(400, f"Maximum number of players {NUM_PLAYERS} is reached")

    address = data["address"]

    print(f"Peer at {address} connected to say hello")
    player.add_peer(address)

    return "ok"


@app.route("/move/", methods=["post"])
def move():
    data = request.get_json()

    if data is None or "address" not in data or "city" not in data:
        abort(400, "Please specify the 'address' and 'city' value")

    address = data["address"]
    city = data["city"]

    if not player.is_move_valid(address, city):
        abort(400)

    print(f"Peer at {address} guessed: {city}")
    player.add_city(city)

    return "ok"


if __name__ == "__main__":
    logging.getLogger("werkzeug").disabled = True
    os.environ["WERKZEUG_RUN_MAIN"] = "true"

    app.run(debug=True, use_reloader=False)
