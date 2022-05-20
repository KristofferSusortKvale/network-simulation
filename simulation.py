from imports.node import node
from imports.user import user
from imports.datetime import get_now

# loop variables
end_of_simulation = False
is_test = False
is_one_cycle = False
simulation_time = 10 # seconds
end_time = get_now() + simulation_time

node = node("127.0.0.1", is_test)
user = user("127.0.0.2", 5)

# Actual loop
while not end_of_simulation:
    # users
    if user.tick():
        user.create_package(node)
        user.new_task()

    # nodes
    node.check_received()
    node.process_package()
    node.send_package()

    if is_one_cycle:
        end_of_simulation = True

    if get_now() > end_time:
        end_of_simulation = True

node.write_results()
user.write_results()
