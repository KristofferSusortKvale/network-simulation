from imports.node import node
from imports.user import user
from imports.datetime import get_now
from numpy.random import randint

# loop variables
end_of_simulation = False
#is_test = False
is_one_cycle = False
simulation_time = 10 # seconds
end_time = get_now() + simulation_time

node1 = node("127.0.0.1", max_send_data_packages=5, pretty_name="1")
node2 = node("127.0.0.3", max_send_data_packages=5, pretty_name="2")
goal = node("127.0.0.4", max_send_data_packages=5, pretty_name="goal")
user = user("127.0.0.2", 5)

# set up lookups
node1.add_lookup_entry(node2.get_ip_address(), node2)
node1.add_lookup_entry(goal.get_ip_address(), goal)
node1.add_lookup_entry(user.get_ip_address(), user)

node2.add_lookup_entry(node1.get_ip_address(), node1)
node2.add_lookup_entry(goal.get_ip_address(), goal)
node2.add_lookup_entry(user.get_ip_address(), user)

goal.add_lookup_entry(user.get_ip_address(), user)

# Actual loop
while not end_of_simulation:
    # users
    if user.tick():
        random_int = randint(2)
        if random_int == 0:
            user.create_package(node1, goal)
        elif random_int == 1:
            user.create_package(node2, goal)
        user.new_task()

    # nodes
    node1.check_received()
    node2.check_received()
    goal.check_received()

    node1.process_package()
    node2.process_package()
    goal.process_package()

    node1.send_package()
    node2.send_package()
    goal.send_package()

    if is_one_cycle:
        end_of_simulation = True

    if get_now() > end_time:
        end_of_simulation = True

node1.write_results()
node2.write_results()
goal.write_results()
user.write_results()
