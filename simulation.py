# from imports/classes/node.py import node

# loop variables
end_of_simulation = False
is_test = False
is_one_cycle = False
simulation_time = 5*60 # seconds
end_time = get_now() + simulation_time
simulation_root_directory = Path.cwd().parents[0]

node = node("127.0.0.1", "unique-string", is_test)

# Actual loop
while not end_of_simulation:
    node.check_received()
    node.process_package()
    #send_package()

    if is_one_cycle:
        end_of_simulation = True

    if get_now() > end_time:
        end_of_simulation = True

node.write_results()
node.clean_up()
