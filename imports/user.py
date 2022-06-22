from imports.datetime import get_now
from numpy.random import exponential
from math import floor
from imports.package import task, ping, data

class user:
    def __init__(self, wait_multiplier=1, task_rate=1, pretty_name=""):
        self._pretty_name = pretty_name
        self._wait_multiplier = wait_multiplier
        self._task_rate = task_rate
        self._next_task = 0
        self._packages_sent = 0
        # self._packages_recieved = 0

    def __str__(self):
        if self._pretty_name == "":
            return "Unnamed User"
        else:
            return "User: " + self._pretty_name

    # def add_package(self, package):
    #     self._packages_recieved += 1 # sink for packages

    def set_new_task_time(self):
        self._next_task = self._wait_multiplier *\
                            floor(exponential(1/self._task_rate))

    def tick(self):
        self._next_task -= 1
        return self._next_task <= 0

    def package_sent(self):
        self._packages_sent += 1

    def get_packages_sent(self):
        return self._packages_sent

    def create_package(self, start, target):
        # Setting sender ip address to start node, simulating that as the
        # device the user sends the request from
        outgoing_package = task(start.get_ip_address(), target.get_ip_address())
        start.task_started()
        start.add_package(outgoing_package)

    def write_results(self):
        result_string = "### Results for " + str(self) + "###\n"
        result_string = "Packages sent: " + str(self._packages_sent) + "\n"
        return result_string
        #print("Packages recieved: ", self._packages_recieved)

def user_results(users):
    result_string = "### User Results ###\n"
    for user in users:
        result_string += user.write_results()
    return result_string
