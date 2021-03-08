from collections import defaultdict

from flask import Flask, abort, jsonify, request

NUM_PLAYERS = 4

app = Flask(__name__)
addresses = defaultdict(list)


@app.route("/rooms/<string:game_id>/join/", methods=["post"])
def register_peer(game_id):
    data = request.get_json()

    if data is None or "address" not in data:
        abort(400, "Please specify the 'address' value")

    address = data["address"]
    peers = addresses[game_id]

    if len(peers) >= NUM_PLAYERS:
        abort(400, f"Maximum number of players {NUM_PLAYERS} is reached")

    peers.append(address)

    return jsonify(peers)


if __name__ == "__main__":
    app.run(debug=True)
