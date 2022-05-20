from imports.datetime import get_now
from numpy.random import exponential
from math import floor
from imports.package import task, ping

class user:
    def __init__(self, ip_address, min_wait, pretty_name=""):
        self._pretty_name = pretty_name
        self._min_wait = min_wait
        self._last_update = get_now()
        self._ip_address = ip_address
        self._next_task = 0
        self._packages_sent = 0
        self._packages_recieved = 0

    def __str__(self):
        if self._pretty_name == "":
            return "Unnamed User"
        else:
            return "User: " + self._pretty_name

    def get_ip_address(self):
        return self._ip_address

    def add_package(self, package):
        self._packages_recieved += 1 # sink for packages

    def new_task(self):
        self._next_task = self._min_wait + floor(exponential())

    def tick(self):
        self._next_task -= 1
        return self._next_task <= 0

    def create_package(self, start, target):
        self._packages_sent += 1

        outgoing_package = task(self._ip_address, target.get_ip_address())
        start.add_package(outgoing_package)

    def write_results(self):
        print("### Results for ", self, "###")
        print("Packages sent: ", self._packages_sent)
        print("Packages recieved: ", self._packages_recieved)
