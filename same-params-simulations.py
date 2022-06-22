from imports.user import user
from imports.simulation import simulation, run_sim
from matplotlib import pyplot as plt

num_simulations = 80

sim_cycles = 5000

num_routers = 30
num_devices_per_router = 10
alt_connections = 30
num_users = 150

user_wait_multiplier = 2000
user_task_rate = 5

users = [ user( pretty_name="User "+str(i),
                wait_multiplier=user_wait_multiplier,
                task_rate=user_task_rate)
                for i in range(num_users)]

ref_results = []
alt_results = []
packages_sent_list = []

for simulation_counter in range(1, num_simulations+1): # 1 indexed
    ref_sim = simulation(number_of_routers=num_routers,
                            number_of_nodes_per_router=num_devices_per_router)

    alt_sim = simulation(number_of_routers=num_routers,
                            number_of_nodes_per_router=num_devices_per_router,
                            is_alt = True, alt_connections=alt_connections)

    print("Starting simulation ", simulation_counter, "...")

    ref_result, alt_result, packages_sent = run_sim(users, ref_sim, alt_sim,
                                                        sim_cycles)

    ref_results.append(ref_result)
    alt_results.append(alt_result)
    packages_sent_list.append(packages_sent)

    print("Results simulation ", simulation_counter, "...")
    print("Ref result: ", ref_result)
    print("Alt result: ", alt_result)
    print("Packages sent: ", packages_sent)
    print("")
