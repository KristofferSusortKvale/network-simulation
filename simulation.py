from imports.node import node
from imports.user import user
from imports.my_datetime import get_now

# loop variables
end_of_simulation = False
is_test = False
is_one_cycle = False
simulation_time = 5*60 # seconds
end_time = get_now() + simulation_time
simulation_root_directory = Path.cwd().parents[0]

node = node("127.0.0.1", "unique-string", is_test)
user = user(5, "127.0.0.2", "other-unique-string")

# Actual loop
while not end_of_simulation:
    # users
    if user.tick():
        user.create_package(node)
        user.new_task()

    # nodes
    node.check_received()
    node.process_package()
    #send_package()

    if is_one_cycle:
        end_of_simulation = True

    if get_now() > end_time:
        end_of_simulation = True

node.write_results()
node.clean_up()
