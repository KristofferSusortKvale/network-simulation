from os import mkdir, listdir, rename, remove
from os.path import isdir, join
from json import loads as parse_json
from json import dumps as create_json
from shutil import rmtree
from pathlib import Path
from datetime import datetime, timedelta
from time import sleep

end_of_simulation = False
is_test = False
is_one_cycle = False
simulation_time = 5*60 # seconds
end_time = datetime.now() + timedelta(0, simulation_time)
simulation_root_directory = Path.cwd().parents[0]

ip_address = "127.0.0.1"
unique_string = "node" # used to create file names
files_created = 0
lookup_table = {}
current_package = {}
outgoing_package = {}
next_target_path = ""

times_incoming_empty = 0
times_current_package_empty = 0


def datetime_to_int(datetime_obj):
    diff = datetime_obj - datetime.min
    return diff.days * 24 * 60 * 60 + diff.seconds

def int_to_datetime(int):
    return datetime.min + timedelta(0, int)


def setup():
    #pass
    mkdir("incoming") # Creates a directory called incoming in relative path




def test_setup():
    content = listdir(simulation_root_directory)

    for i in content:
        if isdir(join(simulation_root_directory, i)):
            print("directory: ", i)

    file = open("incoming/test.json", "w")
    test_package = {
        "header": {
            "sender":"127.0.0.1",
            "target":"127.0.0.1",
            "time": datetime_to_int(datetime.now())
        },
        "payload": {
            "is_task":True,
            "is_ping":False,
            "data":{}
        }
    }
    file.write(create_json(test_package))
    file.close()

    print("time now: ", datetime.now())

def check_received():
    incoming_packages = []
    global times_incoming_empty
    global current_package

    for file in listdir("incoming"):
        if file.endswith(".json"):
            #print("found it", file)
            path = "incoming/" + file
            package = open(path, "r")
            incoming_packages.append(parse_json(package.read()))
            package.close()

    #print(incoming_packages)
    if len(incoming_packages) == 0:
        current_package = {}
        times_incoming_empty += 1
        sleep(1)
    else:
        # sort packages by time
        # print("before: ", incoming_packages)
        # print("Element: ", incoming_packages[0]["header"]["time"])
        # print("sort: ", incoming_packages.sort(
        #     key=lambda p: p["header"]["time"]))
        incoming_packages = sorted(incoming_packages,
            key=lambda p: p["header"]["time"])
        # print("after: ", incoming_packages)
        current_package = incoming_packages[0]
        # print("current package: ", current_package)
        remove(current_package["header"]["path"])


    # print("incoming packages found: ", incoming_packages)
    #
    # try:
    #     print("header: ", incoming_packages[0]["header"])
    # except:
    #     print("header not found")
    #
    # try:
    #     print("sender: ", incoming_packages[0]["header"]["sender"])
    # except:
    #     print("sender not found")

def process_package():
    global outgoing_package

    if current_package == {}:
        #times_current_package_empty += 1
        sleep(1)
    else:
        if current_package["header"]["target"] == ip_address:
            # package to me
            # read package
            if current_package["payload"]["is_task"]:
                # generate data package as response
                print("Task", current_package)
            elif current_package["payload"]["is_ping"]:
                outgoing_package = {
                    "header": {
                        "sender": ip_address,
                        "target": current_package["header"]["sender"],
                        "time": datetime_to_int(datetime.now()),
                        "path": ""
                    },
                    "payload": {
                        "is_task": False,
                        "is_ping": False,
                        "data": {
                            "time_used":
                                datetime_to_int(datetime.now()) \
                                - current_package["header"]["time"]
                        }
                    }
                }
            else:
                # package of data sent to this device
                print("Data recieved", current_package)

        else:
            # package not to this node, forwarding
            print("Forwarding", current_package)
            # set next_target_path using lookup_table
            # set outgoing_package to same content as current_package
            # continue to send_package

def send_package():
    # next_target_path is set
    # outgoing_package is set
    global files_created
    global outgoing_package
    files_created += 1
    filename = "incoming/" + unique_string + str(files_created) + ".json"
    file = open(join(next_target_path, filename), "w")
    outgoing_package["header"]["path"] = filename
    file.write(create_json(outgoing_package))
    file.close()

def write_results():
    print("Files created: ", str(files_created))
    print("Times incoming empty: ", str(times_incoming_empty))

def clean_up():
    print("file in incoming directory on delete: ", listdir("incoming"))
    rmtree("incoming")


# Actual loop
setup()
if is_test:
    test_setup()

while not end_of_simulation:
    check_received()
    process_package()
    #send_package()

    if is_one_cycle:
        end_of_simulation = True

    if datetime.now() > end_time:
        end_of_simulation = True

write_results()
clean_up()
