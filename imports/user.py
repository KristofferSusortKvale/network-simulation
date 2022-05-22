from imports.datetime import get_now
from numpy.random import exponential
from math import floor
from imports.package import task, ping, data

class user:
    def __init__(self, ip_address, min_wait=1, pretty_name=""):
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

        # Setting sender ip address to start node, simulating that as the
        # device the user sends the request from
        outgoing_package = task(start._ip_address, target.get_ip_address())
        start.add_package(outgoing_package)

    def write_results(self):
        print("### Results for ", self, "###")
        print("Packages sent: ", self._packages_sent)
        #print("Packages recieved: ", self._packages_recieved)
