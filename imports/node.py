#from os import mkdir, listdir, rename, remove
#from os.path import isdir, join
#from json import loads as parse_json
#from json import dumps as create_json
#from shutil import rmtree
#from pathlib import Path
#from time import sleep
from imports.datetime import get_now
from imports.package import data


class node:
    def __init__(self, ip_address, unique_string, is_test):
        self.ip_address = ip_address
        # self.unique_string = unique_string
        # self.files_created = 0

        self.lookup_table = {}
        self.package_queue = []
        self.current_package = None
        self.outgoing_package = None
        #self.next_target_path = {}

        self.idle_cycles = 0
        self.packages_sent = 0

        # Changed from incoming to unique string to avoid conflict with others
        #mkdir(unique_string)
        #self.incoming_folder = join(Path.cwd(), unique_string)

        if is_test:
            pass
            # file = open(join(unique_string, "test.json"), "w")
            # test_package = ping(self, self)
            # file.write(create_json(test_package))
            # file.close()

    # def get_incoming_folder(self):
    #     return self.incoming_folder

    def get_ip_address(self):
        return self.ip_address

    def add_package(self, package):
        self.package_queue.append(package)

    def check_received(self):
        # incoming_packages = []
        #
        # for file in listdir(self.incoming_folder):
        #     if file.endswith(".json"):
        #         path = join(self.incoming_folder, file)
        #         package = open(path, "r")
        #         incoming_packages.append(parse_json(package.read()))
        #         package.close()

        if len(self.package_queue) == 0:
            self.current_package = None
            self.idle_cycles += 1
        else:
            # sort packages by time
            self.package_queue = sorted(self.package_queue,
                key=lambda p: p.get_header().get_time())
            self.current_package = self.package_queue.pop(0)
            # remove(self.current_package["header"]["path"]) #fix this


    def process_package(self):
        if self.current_package is not None:
            if self.current_package.get_header().get_target() == self.ip_address:
                # package to me
                # read package
                if self.current_package.get_payload().get_is_task():
                    pass
                    # generate data package as response
                elif self.current_package.get_payload().get_is_ping():

                    time_used = get_now() \
                    - self.current_package.get_header().get_time()

                    data = { "time_used": time_used }

                    self.outgoing_package = data(self.ip_address,
                            self.current_package.get_header().get_sender(),
                            data)
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
        if self.outgoing_package is not None:
            self.packages_sent += 1

            target_node = self.lookup_table[
                            self.outgoing_package.get_header().get_target()]

            target_node.add_package(self.outgoing_package)
            self.outgoing_package = None

        # assumes
        # next_target_path is set and needs to be for target node
        # outgoing_package is set
        # self.files_created += 1
        # filename = self.unique_string + str(files_created) + ".json"
        # file = open(join(self.next_target_path, filename), "w")
        # self.outgoing_package["header"]["path"] = filename
        # file.write(create_json(self.outgoing_package))
        # file.close()

    def write_results(self):
        print("Packages sent: ", str(self.packages_sent))
        print("Idle cycles: ", str(self.idle_cycles))

    def clean_up(self):
        pass
        #print("file in incoming directory on delete: ",
        #        listdir(self.incoming_folder))
        #rmtree(self.incoming_folder)
