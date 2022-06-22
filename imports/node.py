from imports.datetime import get_now
from imports.package import data
from numpy.random import randint


class node:
    def __init__(self, ip_address, parent_simulation,
                    max_send_data_packages=1, is_test=False, pretty_name=""):
        self._pretty_name = pretty_name

        self._parent_simulation = parent_simulation

        self._ip_address = ip_address
        self._max_packages = max_send_data_packages

        self._lookup_table = {}
        self._package_queue = []
        self._current_package = None
        self._outgoing_packages = []

        self._idle_cycles = 0
        self._packages_sent = 0
        self._data_packages_received = 0

        self._tasks_started = 0
        self._tasks_finished = 0

        if is_test:
            pass
            # file = open(join(unique_string, "test.json"), "w")
            # test_package = ping(self, self)
            # file.write(create_json(test_package))
            # file.close()

    def task_started(self):
        self._tasks_started += 1

    def task_finished(self):
        self._tasks_finished += 1

    def __str__(self):
        if self._pretty_name == "":
            return "Unnamed Node"
        else:
            return "Node: " + self._pretty_name

    def get_ip_address(self):
        return self._ip_address

    def add_package(self, package):
        self._package_queue.append(package)

    def remove_lookup_entry(self, ip_address):
        self._lookup_table.pop(ip_address)

    def add_lookup_entry(self, ip_address, node):
        self._lookup_table[ip_address] = node

    def lookup(self, ip_address):
        if "." in ip_address:
            try:
                return self._lookup_table[ip_address]
            except:
                last_dot_index = ip_address.rfind(".")
                return self.lookup(ip_address[:last_dot_index])
        else:
            try:
                return self._lookup_table[ip_address]
            except:
                return -1

    def tick(self):
        for package in self._package_queue:
            package.tick()

        for package in self._outgoing_packages:
            package.tick()

    def check_received(self):
        if len(self._package_queue) == 0:
            self._idle_cycles += 1
        else:
            # sort packages by time
            self._package_queue = sorted(self._package_queue,
                key=lambda p: p.get_header().get_time())
            self._current_package = self._package_queue.pop(0)


    def process_package(self):
        if self._current_package is not None:
            if self._current_package.get_header().get_target() == self._ip_address:
                # package to me
                self._parent_simulation.add_to_sink(self._current_package)
                if self._current_package.get_payload().get_is_task():
                    # generate data package as response
                    num_packages = randint(self._max_packages)
                    for i in range(num_packages):
                        package = data(self._ip_address,
                            self._current_package.get_header().get_sender())
                        self._outgoing_packages.append(package)
                elif self._current_package.get_payload().get_is_ping():
                    # ping, so send data package with time used to get here
                    time_used = get_now() \
                    - self._current_package.get_header().get_time()

                    out_data = { "time_used": time_used }

                    self._outgoing_packages.append(data(self._ip_address,
                            self._current_package.get_header().get_sender(),
                            payload_data=out_data))
                else:
                    self._data_packages_received += 1
                    self.task_finished()
                    # package of data sent to this device

            else:
                pass
                # package not to this node, forwarding
                # set outgoing_package to current_package
                self._outgoing_packages.append(self._current_package)
                # continue to send_package
        self._current_package = None


    def send_package(self):
        if len(self._outgoing_packages) > 0:
            outgoing_package = self._outgoing_packages.pop(0)

            target_ip_address = outgoing_package.get_header().get_target()
            target_node = self.lookup(target_ip_address)

            if target_node == -1:
                print("Node with ip: ", target_ip_address,
                        " not found in lookup table.")
            else:
                target_node.add_package(outgoing_package)
                self._packages_sent += 1

    def write_results(self):
        result_string = "### Results for " +  str(self) + "###\n"
        result_string += "Packages sent: " + str(self._packages_sent) + "\n"
        result_string += "Packages received: " +\
                            str(self._data_packages_received) + "\n"
        result_string += "Idle cycles: " + str(self._idle_cycles) + "\n"
        result_string += "Length incoming queue: " +\
                            str(len(self._package_queue)) + "\n"
        result_string += "Length outgoing queue: " +\
                            str(len(self._outgoing_packages)) + "\n"
        result_string += "Tasks started: " + str(self._tasks_started) + "\n"
        result_string += "Tasks finished: " + str(self._tasks_finished) + "\n"
        return result_string
