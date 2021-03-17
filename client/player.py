import os
from typing import List
from urllib.parse import urljoin
import time
import requests
from client.tasks import timeout_task, app

REGISTRY_ADDRESS = os.environ["REGISTRY_ADDRESS"]
NUM_PLAYERS = int(os.environ["NUM_PLAYERS"])
SELF_ADDRESS = os.getenv("SELF_ADDRESS", f"http://127.0.0.1:{os.environ['PORT']}")
TIME_TO_LOSE = 30


class Player:
    def __init__(self):
        self.peer_addresses = []
        self.cities = []
        self.last_timestamp = None
        self.timeout_task = None

        response = requests.get(
            "https://pkgstore.datahub.io/core/world-cities/world-cities_json/data/5b3dd46ad10990bca47b04b4739a02ba/world-cities_json.json"
        )
        cities = response.json()
        self.valid_cities = [city["name"] for city in cities]

        app.control.purge()

    @property
    def order(self):
        return (
            self.peer_addresses.index(SELF_ADDRESS)
            if SELF_ADDRESS in self.peer_addresses
            else None
        )

    @property
    def lost(self):
        return SELF_ADDRESS not in self.peer_addresses

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
        task_result = timeout_task.apply_async(
            [self.peer_addresses[0]], countdown=TIME_TO_LOSE
        )
        self.timeout_task = task_result

    def is_move_valid(self, address, city, timestamp):
        if self.lost:
            return True, True

        is_order_right = self.move_count % len(
            self.peer_addresses
        ) == self.peer_addresses.index(address)
        is_city_unique = city not in self.cities
        is_city_valid = (
            len(self.cities) == 0 or self.cities[-1][-1].lower() == city[0].lower()
        )

        is_city_name_valid = self._check_city(city)

        now = time.time()
        is_time_correct = timestamp <= now and (
            self.last_timestamp is None
            or timestamp - self.last_timestamp <= TIME_TO_LOSE
        )

        return (
            is_order_right and is_city_unique and is_city_valid and is_city_name_valid,
            not is_time_correct,
        )

    def add_city(self, city, timestamp):
        if self.timeout_task is not None:
            self.timeout_task.revoke()
        self.last_timestamp = timestamp
        self.cities.append(city)

    def move(self, city, timestamp):
        for address in set(self.peer_addresses) - set([SELF_ADDRESS]):
            url = urljoin(address, "/move/")
            response = requests.post(
                url,
                json={"address": SELF_ADDRESS, "city": city, "timestamp": timestamp},
            )
            response.raise_for_status()

    def _check_city(self, name):
        return name in self.valid_cities
