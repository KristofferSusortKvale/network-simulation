from my_datetime import get_now
from numpy.random import exponential
from math import floor
from os.path import join
from json import dumps as create_json

class user:
    def __init__(self, min_wait, ip_address, unique_string):
        self.min_wait = min_wait
        self.last_update = get_now()
        self.ip_address = ip_address
        self.unique_string = unique_string
        self.files_created = 0
        self.next_task = 0

    def new_task(self):
        self.next_task = self.min_wait + floor(exponential())

    def tick(self):
        self.next_task -= 1
        return self.next_task <= 0

    def create_package(self, target):
        self.files_created += 1

        path = join(target.get_incoming_directory(),
            self.unique_string + str(self.files_created) + ".json")

        package = {
            "header": {
                "sender": ip_address,
                "target": target.get_ip_address(),
                "time": get_now(),
                "path": path
            },
            "payload": {
                "is_task": True,
                "is_ping": False,
                "data": {}
            }
        }

        file = open(path, "w")
        file.write(create_json(package))
        file.close()
