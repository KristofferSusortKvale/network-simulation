from datetime import datetime, timedelta
from time import sleep
from numpy.random import exponential, randint
#from math import floor
from json import dumps as create_json

simulation_time = 4*60
end_time = datetime.now() + timedelta(0, simulation_time)
min_wait = 5.0 # 5 seconds
last_datetime = datetime.now()
ip_address = "127.0.0.2"
targets = ["127.0.0.1"]

unique_string = "user" # used to create file names
files_created = 0


# import function
def datetime_to_int(datetime_obj):
    diff = datetime_obj - datetime.min
    return diff.days * 24 * 60 * 60 + diff.seconds


def new_wait():
    return min_wait + exponential(scale=1000) / 1000


#wait_time = new_wait()
wait_time = 1.0

def random_target():
    return targets[randint(len(targets))]

def create_package(files_created, unique_string):
    files_created += 1
    time_now = datetime_to_int(datetime.now())
    print(time_now)
    path = "incoming/" + unique_string + str(files_created) + ".json"
    package = {
        "header": {
            "sender": ip_address,
            "target": random_target(),
            "time": time_now,
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

    return files_created



while datetime.now() < end_time:
    sleep(wait_time)
    files_created = create_package(files_created, unique_string)
    wait_time = new_wait()
