from imports.datetime import get_now
from numpy.random import exponential
from math import floor
from imports.package import task

class user:
    def __init__(self, ip_address, min_wait):
        self.min_wait = min_wait
        self.last_update = get_now()
        self.ip_address = ip_address
        self.next_task = 0
        self.packages_sent = 0
        self.packages_recieved = 0

    def get_ip_address(self):
        return self.ip_address

    def add_package(self):
        self.packages_recieved += 1 # sink for packages

    def new_task(self):
        self.next_task = self.min_wait + floor(exponential())

    def tick(self):
        self.next_task -= 1
        return self.next_task <= 0

    def create_package(self, target):
        self.packages_sent += 1

        outgoing_package = task(self, target)
        target.add_package(outgoing_package)

    def write_results(self):
        print("Packages sent: ", self.packages_sent)
        print("Packages recieved: ", self.packages_recieved)
