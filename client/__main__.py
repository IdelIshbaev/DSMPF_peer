import logging
import os
import requests
from collections import defaultdict

from flask import Flask, abort, jsonify, request
from client.tasks import timeout_task
from client.player import Player
import time

NUM_PLAYERS = int(os.environ["NUM_PLAYERS"])
SELF_ADDRESS = os.getenv("SELF_ADDRESS", f"http://127.0.0.1:{os.environ['PORT']}")
TIME_TO_LOSE = 30

app = Flask(__name__)
player = Player()


def run_timeout_task(address):
    task_result = timeout_task.apply_async([address], countdown=TIME_TO_LOSE)
    player.timeout_task = task_result


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

    if (
        data is None
        or "address" not in data
        or "city" not in data
        or "timestamp" not in data
    ):
        abort(400, "Please specify the 'address' and 'city' value")

    address = data["address"]
    city = data["city"]
    timestamp = data["timestamp"]

    if address not in player.peer_addresses:
        abort(400)

    is_city_valid, timed_out = player.is_move_valid(address, city, timestamp)

    if not is_city_valid:
        abort(400)

    if timed_out:
        player.peer_addresses.remove(address)
        abort(401)

    player.add_city(city, timestamp)

    current_player_idx = player.peer_addresses.index(address)
    next_peer = player.peer_addresses[
        (current_player_idx + 1) % len(player.peer_addresses)
    ]
    run_timeout_task(next_peer)

    return "ok"


@app.route("/self_move/", methods=["post"])
def self_move():
    data = request.get_json()

    if data is None or "city" not in data:
        abort(400, "Please specify the 'city' value")

    city = data["city"]
    timestamp = time.time()

    is_city_valid, timed_out = player.is_move_valid(SELF_ADDRESS, city, timestamp)

    if not is_city_valid:
        abort(400)

    if timed_out:
        abort(401)

    player.move(city, timestamp)
    player.add_city(city, timestamp)

    current_player_idx = player.peer_addresses.index(SELF_ADDRESS)
    next_peer = player.peer_addresses[
        (current_player_idx + 1) % len(player.peer_addresses)
    ]
    run_timeout_task(next_peer)

    return "ok"


@app.route("/timeout/", methods=["post"])
def timeout():
    data = request.get_json()
    address = data["address"]

    if player.lost or address not in player.peer_addresses:
        return "ok"

    current_player_idx = player.peer_addresses.index(address)
    next_peer = player.peer_addresses[
        (current_player_idx + 1) % len(player.peer_addresses)
    ]

    run_timeout_task(next_peer)
    player.peer_addresses.remove(address)

    player.last_timestamp = time.time()

    return "ok"


@app.route("/join/", methods=["post"])
def join():
    data = request.get_json()

    if data is None or "game_id" not in data:
        abort(400, "Please specify the 'game_id'")

    game_id = data["game_id"]
    player.join_game(game_id)

    return "ok"


@app.route("/status", methods=["get"])
def status():
    data = request.get_json()

    return jsonify(
        {
            "peers": player.peer_addresses,
            "cities": player.cities,
            "order": player.order,
        }
    )


if __name__ == "__main__":
    logging.getLogger("werkzeug").disabled = True
    os.environ["WERKZEUG_RUN_MAIN"] = "true"

    app.run(debug=True, use_reloader=False, port=os.getenv("PORT", 5000))
