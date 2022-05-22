from imports.node import node
from imports.user import user
from imports.datetime import get_now
from imports.network import routers_and_nodes
from numpy.random import randint

k = 1000
M = k*k
G = k*M
T = k*G

# loop variables
end_of_simulation = False
#is_test = False
is_one_cycle = False

is_time_based = False
simulation_time = 10 # seconds
end_time = get_now() + simulation_time

simulation_cycles = k

number_of_routers = 5
number_of_nodes_per_router = 5
max_send_data_packages = 5

number_of_users = 50

# Create router nodes
routers = [node(str(i), pretty_name="Router " + str(i))
            for i in range(number_of_routers)]

# Nested list of device nodes, one list per router
# Inner list is list of device nodes of length number_of_nodes_per_router

devices = [[
    # node
    node(str(i)+"."+str(j), max_send_data_packages=max_send_data_packages,
            pretty_name="Device " + str(i)+"."+str(j))
        # inner list of nodes (one list per router)
        for j in range(number_of_nodes_per_router)]
            # outer list of list of nodes
            for i in range(number_of_routers)]

# connect routers and devices
routers_and_nodes(routers, devices)
# from here routers are also in devices list

# flatten devices list
devices = [node for list_of_nodes in devices for node in list_of_nodes]

# Create users
users = [user(str(number_of_routers)+"."+str(i), pretty_name="User "+str(i))
            for i in range(number_of_users)]

# IP of users??????
# user connection???

# node1 = node("127.0.0.1", max_send_data_packages=5, pretty_name="1")
# node2 = node("127.0.0.3", max_send_data_packages=5, pretty_name="2")
# goal = node("127.0.0.4", max_send_data_packages=5, pretty_name="goal")
# user = user("127.0.0.2", 5)
#
# # set up lookups
# node1.add_lookup_entry(node2.get_ip_address(), node2)
# node1.add_lookup_entry(goal.get_ip_address(), goal)
# node1.add_lookup_entry(user.get_ip_address(), user)
#
# node2.add_lookup_entry(node1.get_ip_address(), node1)
# node2.add_lookup_entry(goal.get_ip_address(), goal)
# node2.add_lookup_entry(user.get_ip_address(), user)
#
# goal.add_lookup_entry(user.get_ip_address(), user)

# Actual loop
while not end_of_simulation:
    # users
    for user in users:
        if user.tick():
            random_start_node = randint(len(devices))
            random_goal_node = randint(len(devices))
            user.create_package(devices[random_start_node],
                                devices[random_goal_node])
            user.new_task()

    # nodes
    for device in devices:
        device.check_received()
        device.process_package()
        device.send_package()

    # routers are in devices list
    # for router in routers:
    #     router.check_received()
    #     router.process_package()
    #     router.send_package()

    if is_one_cycle:
        end_of_simulation = True

    if is_time_based and get_now() > end_time:
        end_of_simulation = True

    if not is_time_based:
        simulation_cycles -= 1
        if simulation_cycles <= 0:
            end_of_simulation = True

# for user in users:
#     user.write_results()

# for router in routers:
#     router.write_results()

for device in devices:
    device.write_results()
