from imports.datetime import get_now
from os.path import join

class header:
    def __init__(self, sender, target, time):
        self._sender = sender
        self._target = target
        self._time = time

    def get_time(self):
        return self._time

    def get_target(self):
        return self._target

    def get_sender(self):
        return self._sender


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
