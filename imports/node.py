from imports.datetime import get_now
from imports.package import data


class node:
    def __init__(self, ip_address, is_test):
        self.ip_address = ip_address

        self.lookup_table = {}
        self.package_queue = []
        self.current_package = None
        self.outgoing_package = None

        self.idle_cycles = 0
        self.packages_sent = 0

        if is_test:
            pass
            # file = open(join(unique_string, "test.json"), "w")
            # test_package = ping(self, self)
            # file.write(create_json(test_package))
            # file.close()

    def get_ip_address(self):
        return self.ip_address

    def add_package(self, package):
        self.package_queue.append(package)

    def check_received(self):

        if len(self.package_queue) == 0:
            self.current_package = None
            self.idle_cycles += 1
        else:
            # sort packages by time
            self.package_queue = sorted(self.package_queue,
                key=lambda p: p.get_header().get_time())
            self.current_package = self.package_queue.pop(0)


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

    def write_results(self):
        print("Packages sent: ", str(self.packages_sent))
        print("Idle cycles: ", str(self.idle_cycles))
