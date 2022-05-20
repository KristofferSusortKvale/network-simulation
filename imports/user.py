from imports.datetime import get_now
from numpy.random import exponential
from math import floor
from imports.package import task

class user:
    def __init__(self, ip_address, min_wait):
        self._min_wait = min_wait
        self._last_update = get_now()
        self._ip_address = ip_address
        self._next_task = 0
        self._packages_sent = 0
        self._packages_recieved = 0

    def get_ip_address(self):
        return self._ip_address

    def add_package(self):
        self._packages_recieved += 1 # sink for packages

    def new_task(self):
        self._next_task = self._min_wait + floor(exponential())

    def tick(self):
        self._next_task -= 1
        return self._next_task <= 0

    def create_package(self, target):
        self._packages_sent += 1

        outgoing_package = task(self, target)
        target.add_package(outgoing_package)

    def write_results(self):
        print("Packages sent: ", self._packages_sent)
        print("Packages recieved: ", self._packages_recieved)
