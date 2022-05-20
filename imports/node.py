from imports.datetime import get_now
from imports.package import data


class node:
    def __init__(self, ip_address, is_test):
        self._ip_address = ip_address

        self._lookup_table = {}
        self._package_queue = []
        self._current_package = None
        self._outgoing_package = None

        self._idle_cycles = 0
        self._packages_sent = 0

        if is_test:
            pass
            # file = open(join(unique_string, "test.json"), "w")
            # test_package = ping(self, self)
            # file.write(create_json(test_package))
            # file.close()

    def get_ip_address(self):
        return self._ip_address

    def add_package(self, package):
        self._package_queue.append(package)

    def check_received(self):

        if len(self._package_queue) == 0:
            self._current_package = None
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
                # read package
                if self._current_package.get_payload().get_is_task():
                    pass
                    # generate data package as response
                elif self._current_package.get_payload().get_is_ping():

                    time_used = get_now() \
                    - self._current_package.get_header().get_time()

                    data = { "time_used": time_used }

                    self._outgoing_package = data(self._ip_address,
                            self._current_package.get_header().get_sender(),
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
        if self._outgoing_package is not None:
            self._packages_sent += 1

            target_node = self._lookup_table[
                            self._outgoing_package.get_header().get_target()]

            target_node.add_package(self._outgoing_package)
            self._outgoing_package = None

    def write_results(self):
        print("Packages sent: ", str(self._packages_sent))
        print("Idle cycles: ", str(self._idle_cycles))
