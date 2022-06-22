from imports.user import user
from imports.simulation import simulation, run_sim


sim_cycles = 5000

base_num_routers = 30
base_num_devices_per_router = 10
base_alt_connections = 30 # 10% of total number of devices

user_wait_multiplier = 2000
user_task_rate = 5

ref_sim = simulation(number_of_routers=base_num_routers,
                        number_of_nodes_per_router=base_num_devices_per_router)

alt_sim = simulation(number_of_routers=base_num_routers,
                        number_of_nodes_per_router=base_num_devices_per_router,
                        is_alt = True, alt_connections=base_alt_connections)

number_of_users_list = [30, 60, 90, 120, 150]

list_of_list_of_users = []

for num_of_users in number_of_users_list:
    users = [ user( pretty_name="User "+str(i),
                    wait_multiplier=user_wait_multiplier,
                    task_rate=user_task_rate)
                    for i in range(num_of_users)]
    list_of_list_of_users.append(users)

print("Number of users simulation starting...")

for users_list in list_of_list_of_users:
    print("Starting simulation for ", len(users_list), " users...")
    ref_result, alt_result, packages_sent = run_sim(users_list,
                                                    ref_sim, alt_sim,
                                                    sim_cycles)
    print("Results for ", len(users_list), " users:")
    print("Ref result: ", ref_result)
    print("Alt result: ", alt_result)
    print("Packages sent: ", packages_sent)
    print("")
