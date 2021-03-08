import os
from typing import List
from urllib.parse import urljoin

import requests

REGISTRY_ADDRESS = os.environ["REGISTRY_ADDRESS"]
NUM_PLAYERS = os.environ["NUM_PLAYERS"]
SELF_ADDRESS = os.environ["SELF_ADDRESS"]


class Player:
    def __init__(self):
        self.peer_addresses = []
        self.cities = []

    @property
    def order(self):
        return self.peer_addresses.index(SELF_ADDRESS)

    @property
    def move_count(self):
        return len(self.cities)

    def join_game(self, game_id):
        url = urljoin(REGISTRY_ADDRESS, f"/rooms/{game_id}/join/")
        response = requests.post(url, json={"address": SELF_ADDRESS})

        response.raise_for_status()

        self.peer_addresses = response.json()

        print(
            f"Connected a registry at {REGISTRY_ADDRESS}, peers returned: {self.peer_addresses}"
        )

        self.notify_peers()

    def notify_peers(self):
        for address in self.peer_addresses:
            if address != SELF_ADDRESS:
                url = urljoin(address, "/hey/")
                response = requests.post(url, json={"address": SELF_ADDRESS})
                response.raise_for_status()
                print(f"Connected a peer at {address} to say hello")

        if len(self.peer_addresses) >= NUM_PLAYERS:
            self.start_game()

    def add_peer(self, address):
        if address not in self.peer_addresses:
            self.peer_addresses.append(address)

        if len(self.peer_addresses) >= NUM_PLAYERS:
            self.start_game()

    def start_game(self):
        print(f"Let the game begin! Your order is {self.order}")

    def is_move_valid(self, address, city):
        is_order_right = self.move_count % NUM_PLAYERS == self.peer_addresses.index(
            address
        )
        is_city_unique = city not in self.cities
        is_city_valid = (
            len(self.cities) == 0 or self.cities[-1][-1].lower() == city[0].lower()
        )

        return is_order_right and is_city_unique and is_city_valid

    def add_city(self, city):
        self.cities.append(city)

    def move(self, city):
        for address in self.peer_addresses:
            url = urljoin(address, "/move/")
            response = requests.post(url, json={"address": SELF_ADDRESS, "city": city})
            response.raise_for_status()
