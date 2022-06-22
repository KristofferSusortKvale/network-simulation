from imports.node import node
from imports.user import user
from imports.network import routers_and_nodes, routers_and_nodes_alt
from imports.network import network_results
from imports.package import package_results
from imports.datetime import get_now
from numpy import sum
from numpy.random import randint

"""
File imports/simulation.py
class simulation
options:
is_alt: boolean, wether alternative connections should be added.
alt_connections: int, number of alternative connections to make (if is_alt=true)
number_of_routers: int, number of router nodes to make
number_of_nodes_per_router: int, number of nodes to make per router
max_send_data_packages: int, maximum number of data packages generated per task

description:
The simulation class handles one simulation of a network of nodes. It has a set
of routers and devices. The network created has the routers connected in a line,
and the nodes are connected to all other nodes for the same router as well as
the router. For nodes not connected to the same router it will send it to its
router.

Methods:
Tick:
All nodes get a tick call
All routers get a tick call
All nodes call check_received, process_package and send_package
All routers call check_received, process_package and send_package


Function simulation_results:
Returns a string with results from the routers, nodes and packages that got to
the package_sink. The package sink is where data packages are placed when
recieved by the goal node.
"""

class simulation:
    def __init__(self, name="Simulation",
        is_alt = False, alt_connections = 0,
        number_of_routers = 1, number_of_nodes_per_router = 1,
        max_send_data_packages = 5):
        self._name = name
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

        if is_alt:
            routers_and_nodes_alt(self._routers, self._devices, alt_connections)
        else:
            routers_and_nodes(self._routers, self._devices)

        self._devices = [
            node for list_of_nodes in self._devices for node in list_of_nodes]

        self._package_sink = []

    def __str__(self):
        return self._name

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

    def get_device_by_ip(self, ip):
        for device in self._devices:
            if device.get_ip_address() == ip:
                return device
        return -1


def run_sim(users, ref_simulation, alt_simulation, simulation_cycles):
    simulations = [ref_simulation, alt_simulation]
    end_of_simulation = False
    packages_sent_before = sum([user.get_packages_sent() for user in users])
    while not end_of_simulation:
        for user in users:
            if user.tick():
                random_start_node = randint(len(simulations[0].get_devices()))
                random_goal_node = randint(len(simulations[0].get_devices()))

                start_node_sim1 = simulations[0].get_devices()[random_start_node]
                goal_node_sim1 = simulations[0].get_devices()[random_goal_node]
                user.create_package(start_node_sim1, goal_node_sim1)

                for i in range(1, len(simulations)):
                    sim = simulations[i]
                    start_node = sim.get_device_by_ip(
                                        start_node_sim1.get_ip_address())
                    goal_node = sim.get_device_by_ip(
                                        goal_node_sim1.get_ip_address())
                    user.create_package(start_node, goal_node)

                user.package_sent()

                user.set_new_task_time()

        for sim in simulations:
            sim.tick()

        simulation_cycles -= 1
        if simulation_cycles <= 0:
            end_of_simulation = True

    packages_sent_after = sum([user.get_packages_sent() for user in users])
    packages_sent = packages_sent_after - packages_sent_before

    return len(ref_simulation.get_sink_packages()),\
            len(alt_simulation.get_sink_packages()), \
            packages_sent


def simulation_results(sim, sim_name):
    result_string = "########################################################\n"
    result_string += "Results for simulation "
    result_string += sim_name + "\n"
    result_string += "########################################################"
    result_string += network_results(sim.get_routers())
    result_string += network_results(sim.get_devices())
    result_string += package_results(sim.get_sink_packages())
    result_string += "--------------------------------------------------------"
    result_string += ""
    return result_string
