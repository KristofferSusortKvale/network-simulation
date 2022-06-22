from imports.user import user
from imports.simulation import simulation, run_sim
from numpy.random import randint
from numpy import sum
from math import ceil


sim_cycles = [5000]

user_wait_multipliers = [5]
user_task_rates = [5]
num_users_list = [5]

num_routers_list = [50]
num_devices_per_router_list = [50]
alt_connections_list = [0.01]

results = open("results_test.csv", "w")

results.write("cycles, wait_multiplier, task_rate, num_users, num_routers, \
num_devices_per_router, alt_connections, ref_result, alt_result, packages_sent\n")

result_line = ""
for cycles in sim_cycles:
    for wait_multiplier in user_wait_multipliers:
        for task_rate in user_task_rates:
            for num_users in num_users_list:
                users = [
                    user(wait_multiplier=wait_multiplier, task_rate=task_rate)
                    for i in range(num_users)]
                for num_routers in num_routers_list:
                    for num_devices_per_router in num_devices_per_router_list:
                        num_devices_total = num_devices_per_router * num_routers
                        values_alt_connections = [ceil(num_devices_total * rate)
                                            for rate in alt_connections_list]
                        for alt_connections in values_alt_connections:
                            ref_sim = simulation(number_of_routers=num_routers,
                            number_of_nodes_per_router=num_devices_per_router)
                            alt_sim = simulation(number_of_routers=num_routers,
                            number_of_nodes_per_router=num_devices_per_router,
                            is_alt = True, alt_connections=alt_connections)

                            ref_result, alt_result, packages_sent = run_sim(
                                users, ref_sim, alt_sim, cycles
                            )

                            results.write(str(cycles) + ", "\
                                        + str(wait_multiplier) + ", "\
                                        + str(task_rate) + ", "\
                                        + str(num_users) + ", "\
                                        + str(num_routers) + ", "\
                                        + str(num_devices_per_router) + ", "\
                                        + str(alt_connections) + ", "\
                                        + str(ref_result) + ", "\
                                        + str(alt_result) + ", "\
                                        + str(packages_sent) + "\n")

results.close()
