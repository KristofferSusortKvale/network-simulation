from imports.user import user
from imports.simulation import simulation, run_sim
from matplotlib import pyplot as plt


sim_cycles = 5000

user_wait_multiplier = 1
user_task_rate = 1
num_users = 5

num_routers = 5
num_devices_per_router_list = [5, 50, 500]
alt_connections = 5

ref_results = []
alt_results = []

users = [ user(wait_multiplier=user_wait_multiplier,
                task_rate=user_task_rate)
                for i in range(num_users)]

for num_devices_per_router in num_devices_per_router_list:
    ref_sim = simulation(number_of_routers=num_routers,
                            number_of_nodes_per_router=num_devices_per_router)

    alt_sim = simulation(number_of_routers=num_routers,
                            number_of_nodes_per_router=num_devices_per_router,
                            is_alt = True, alt_connections=alt_connections)

    ref_result, alt_result, packages_sent = run_sim(users, ref_sim, alt_sim,
                                                        sim_cycles)

    ref_results.append(ref_result)
    alt_results.append(alt_result)

plt.bar([str(ele) for ele in num_devices_per_router_list], ref_results)
plt.xlabel("Number of devices per router")
plt.ylabel("Packages completed")
plt.savefig("reference_results_devices")
#plt.show()

plt.bar([str(ele) for ele in num_devices_per_router_list], alt_results)
plt.xlabel("Number of devices per router")
plt.ylabel("Packages completed")
plt.savefig("alternative_results_devices")
#plt.show()
