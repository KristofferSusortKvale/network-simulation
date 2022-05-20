from os import mkdir, listdir, rename, remove
from os.path import isdir, join
from json import loads as parse_json
from json import dumps as create_json
from shutil import rmtree
from pathlib import Path
from time import sleep
# from ../functions/timedate.py import get_now()


class node:
    def __init__(self, ip_address, unique_string, is_test):
        self.ip_address = ip_address
        self.unique_string = unique_string
        self.files_created = 0

        self.lookup_table = {}
        self.current_package = {}
        self.outgoing_package = {}
        self.next_target_path = {}

        self.idle_cycles = 0

        # Changed from incoming to unique string to avoid conflict with others
        mkdir(unique_string)
        self.incoming_folder = join(Path.cwd(), unique_string)

        if is_test:
            file = open(join(unique_string, "test.json"), "w")
            test_package = {
                "header": {
                    "sender":"127.0.0.1",
                    "target":"127.0.0.1",
                    "time": get_now()
                },
                "payload": {
                    "is_task":True,
                    "is_ping":False,
                    "data":{}
                }
            }
            file.write(create_json(test_package))
            file.close()


    def check_received(self):
        incoming_packages = []

        for file in listdir(self.incoming_folder):
            if file.endswith(".json"):
                path = self.incoming_folder + file
                package = open(path, "r")
                incoming_packages.append(parse_json(package.read()))
                package.close()

        if len(incoming_packages) == 0:
            self.current_package = {}
            self.idle_cycles += 1
        else:
            # sort packages by time
            incoming_packages = sorted(incoming_packages,
                key=lambda p: p["header"]["time"])
            self.current_package = incoming_packages[0]
            remove(current_package["header"]["path"])


    def process_package(self):
        if not current_package == {}:
            if current_package["header"]["target"] == ip_address:
                # package to me
                # read package
                if current_package["payload"]["is_task"]:
                    pass
                    # generate data package as response
                elif current_package["payload"]["is_ping"]:
                    outgoing_package = {
                        "header": {
                            "sender": ip_address,
                            "target": current_package["header"]["sender"],
                            "time": get_now(),
                            "path": ""
                        },
                        "payload": {
                            "is_task": False,
                            "is_ping": False,
                            "data": {
                                "time_used":
                                    get_now() \
                                    - self.current_package["header"]["time"]
                            }
                        }
                    }
                else:
                    pass
                    # package of data sent to this device

            else:
                pass
                # package not to this node, forwarding
                # set next_target_path using lookup_table
                # set outgoing_package to same content as current_package
                # continue to send_package


    def send_package(self):
        # assumes
        # next_target_path is set and needs to be for target node
        # outgoing_package is set
        self.files_created += 1
        filename = unique_string + str(files_created) + ".json"
        file = open(join(self.next_target_path, filename), "w")
        outgoing_package["header"]["path"] = filename
        file.write(create_json(outgoing_package))
        file.close()

    def write_results(self):
        print("Files created: ", str(self.files_created))
        print("Idle cycles: ", str(self.idle_cycles))

    def clean_up(self):
        print("file in incoming directory on delete: ",
                listdir(self.incoming_folder))
        rmtree(self.incoming_folder)
