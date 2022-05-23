from imports.node import node
from imports.user import user
from imports.network import routers_and_nodes
from imports.datetime import get_now

class simulation:
    def __init__(self,
        is_alt = False,
        number_of_routers = 2, number_of_nodes_per_router = 5,
        max_send_data_packages = 5):
        self._number_of_routers = number_of_routers
        self._number_of_nodes_per_router = number_of_nodes_per_router
        self._max_send_data_packages = max_send_data_packages

        self._routers = [node(str(i), self, pretty_name="Router " + str(i))
                    for i in range(number_of_routers)]

        self._devices = [[
            # node
            node(str(i)+"."+str(j), self,
                    max_send_data_packages=max_send_data_packages,
                    pretty_name="Device " + str(i)+"."+str(j))
                # inner list of nodes (one list per router)
                for j in range(number_of_nodes_per_router)]
                    # outer list of list of nodes
                    for i in range(number_of_routers)]

        routers_and_nodes(self._routers, self._devices)

        self._devices = [
            node for list_of_nodes in self._devices for node in list_of_nodes]

        self._package_sink = []

    def add_to_sink(self, package):
        self._package_sink.append(package)

    def get_sink_packages(self):
        return self._package_sink

    def tick(self):
        for device in self._devices:
            device.tick()

        for router in self._routers:
            router.tick()

        for device in self._devices:
            device.check_received()
            device.process_package()
            device.send_package()

        for router in self._routers:
            router.check_received()
            router.process_package()
            router.send_package()

    def get_devices(self):
        return self._devices

    def get_routers(self):
        return self._routers
