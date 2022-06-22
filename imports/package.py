from imports.datetime import get_now
from numpy import sum

class header:
    def __init__(self, sender, target, time):
        self._sender = sender
        self._target = target
        self._time = time
        self._ticks_alive = 0

    def get_time(self):
        return self._time

    def get_target(self):
        return self._target

    def get_sender(self):
        return self._sender

    def get_ticks(self):
        return self._ticks_alive

    def tick(self):
        self._ticks_alive += 1


class payload:
    def __init__(self, is_task, is_ping, data):
        self._is_task = is_task
        self._is_ping = is_ping
        self._data = data

    def get_is_task(self):
        return self._is_task

    def get_is_ping(self):
        return self._is_ping


class package:
    def __init__(self, header, payload):
        self._header = header
        self._payload = payload

    def get_header(self):
        return self._header

    def get_payload(self):
        return self._payload

    def tick(self):
        self._header.tick()


def ping(sender_ip_address, target_ip_address):
    t_header = header(
                    sender_ip_address,
                    target_ip_address,
                    get_now())
    t_payload = payload(False, True, {})
    return package(t_header, t_payload)

def task(sender_ip_address, target_ip_address):
    t_header = header(
                    sender_ip_address,
                    target_ip_address,
                    get_now())
    t_payload = payload(True, False, {})
    return package(t_header, t_payload)

def data(sender_ip_address, target_ip_address, payload_data={}):
    t_header = header(
                    sender_ip_address,
                    target_ip_address,
                    get_now())
    t_payload = payload(False, False, payload_data)
    return package(t_header, t_payload)

def package_results(packages):
    if len(packages) == 0:
        return "No packages in list"
    result_string = "### Package Results ###\n"
    num_packages = len(packages)
    result_string += "Number of packages = " + str(num_packages) + "\n"
    package_ticks = [package.get_header().get_ticks()
                        for package in packages]
    avg_ticks = sum(package_ticks) / num_packages
    result_string += "Average ticks alive = " + str(avg_ticks) + "\n"
    return result_string
