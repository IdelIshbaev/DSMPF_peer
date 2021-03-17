import requests
import os
from urllib.parse import urljoin
from time import sleep

NUM_PLAYERS = int(os.environ["NUM_PLAYERS"])

SELF_ADDRESS = os.getenv("SELF_ADDRESS", f"http://127.0.0.1:{os.environ['PORT']}")

JOIN_ADDRESS = urljoin(SELF_ADDRESS, "/join/")
STATUS_ADDRESS = urljoin(SELF_ADDRESS, "/status")
MOVE_ADDRESS = urljoin(SELF_ADDRESS, "/self_move/")

if __name__ == "__main__":
    print("Hi! Let's play a game of cities")

    game_id = input("Please provide a game id: ")

    requests.post(JOIN_ADDRESS, json={"game_id": game_id})

    print("Waiting for game to start...")

    response = requests.get(STATUS_ADDRESS)
    status = response.json()

    while len(status["peers"]) < NUM_PLAYERS:
        sleep(3)
        response = requests.get(STATUS_ADDRESS)
        status = response.json()

    order = status["order"]
    print(f"Let the game start! Your order is {order + 1}")

    old_cities = status["cities"]
    old_peers = status["peers"]
    lost = False
    won = False
    while not (lost or won):
        sleep(2)
        response = requests.get(STATUS_ADDRESS)
        status = response.json()

        cities = status["cities"]
        peers = status["peers"]
        order = status["order"]

        if order is None or SELF_ADDRESS not in peers:
            lost = True
            break

        if peers == [SELF_ADDRESS]:
            won = True
            break

        if peers != old_peers:
            print(
                f"❌ One of the player timed out! There are only {len(peers)} players remaining."
            )

        if cities != old_cities and len(cities) % len(peers) != order + 1:
            print(f"🏙️  Someone guessed a city: {cities[-1]}")

        if len(cities) % len(peers) == order:
            if len(cities) == 0:
                city = input("👉 It's your turn, please enter a city: ")
            else:
                city = input(
                    f"👉 It's your turn, the last city is {cities[-1]}. Please enter a city: "
                )

            response = requests.post(MOVE_ADDRESS, json={"city": city})
            while response.status_code != 200:
                if response.status_code == 401:
                    lost = True
                    break
                city = input("Your guess is rejected, please try again: ")
                response = requests.post(MOVE_ADDRESS, json={"city": city})

            cities.append(city)
            if not lost:
                print("Your guess is accepted! Please wait for your next turn...")

        old_cities = list(cities)
        old_peers = list(peers)

    if won:
        print("🎉 Congratulations! You won this round!")

    if lost:
        print("😞 You lost this time! Try to be faster next time...")
