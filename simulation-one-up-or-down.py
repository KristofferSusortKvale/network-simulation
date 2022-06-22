from imports.user import user
from imports.simulation import simulation, run_sim
from numpy.random import randint
from numpy import sum


sim_cycles = 5000

base_num_routers = 30
base_num_devices_per_router = 10
base_alt_connections = 30 # 10% of total number of devices
base_num_users = 168 # 50% of total number of devices

user_wait_multiplier = 2000
user_task_rate = 5

base_users = [ user( pretty_name="User "+str(i),
                wait_multiplier=user_wait_multiplier,
                task_rate=user_task_rate)
                for i in range(base_num_users)]

base_ref_sim = simulation(number_of_routers=base_num_routers,
                        number_of_nodes_per_router=base_num_devices_per_router)

base_alt_sim = simulation(number_of_routers=base_num_routers,
                        number_of_nodes_per_router=base_num_devices_per_router,
                        is_alt = True, alt_connections=base_alt_connections)

base_simulations = [base_ref_sim, base_alt_sim]

# Baseline results
print("Running base simulation...")
base_ref_result, base_alt_result, base_packages_sent = run_sim(base_users,
                                                    base_ref_sim, base_alt_sim,
                                                    sim_cycles)
print("Base Results:")
print("Ref result: ", base_ref_result)
print("Alt result: ", base_alt_result)
print("Packages sent: ", base_packages_sent)
print("")


# Number of users test
less_users = base_users.copy()
less_users.pop() #remove one user

user_ref_sim = simulation(number_of_routers=base_num_routers,
                        number_of_nodes_per_router=base_num_devices_per_router)
user_alt_sim = simulation(number_of_routers=base_num_routers,
                        number_of_nodes_per_router=base_num_devices_per_router,
                        is_alt = True, alt_connections=base_alt_connections)

print("Running one less user test...")
user_ref_result, user_alt_result, user_packages_sent = run_sim(less_users,
                                                    user_ref_sim, user_alt_sim,
                                                    sim_cycles)
user_ref_diff = user_ref_result - base_ref_result
user_alt_diff = user_alt_result - base_alt_result

print("One less user results:")
print("Ref results: ", user_ref_result, ", difference: ", user_ref_diff)
print("Alt results: ", user_alt_result, ", difference: ", user_alt_diff)
print("Packages sent: ", user_packages_sent)
print("")


# Number of routers test
router_ref_sim = simulation(number_of_routers=base_num_routers-1,
                        number_of_nodes_per_router=base_num_devices_per_router)
router_alt_sim = simulation(number_of_routers=base_num_routers-1,
                        number_of_nodes_per_router=base_num_devices_per_router,
                        is_alt = True, alt_connections=base_alt_connections)

print("Running one less router test...")
router_ref_result, router_alt_result, router_packages_sent = run_sim(base_users,
                                            router_ref_sim, router_alt_sim,
                                            sim_cycles)
router_ref_diff = router_ref_result - base_ref_result
router_alt_diff = router_alt_result - base_alt_result

print("One less router results:")
print("Ref results: ", router_ref_result, ", difference: ", router_ref_diff)
print("Alt results: ", router_alt_result, ", difference: ", router_alt_diff)
print("Packages sent: ", router_packages_sent)
print("")


# Number of devices per router test
devices_ref_sim = simulation(number_of_routers=base_num_routers,
                        number_of_nodes_per_router=base_num_devices_per_router-1)
devices_alt_sim = simulation(number_of_routers=base_num_routers,
                        number_of_nodes_per_router=base_num_devices_per_router-1,
                        is_alt = True, alt_connections=base_alt_connections)
print("Running one less device per router test...")
devices_ref_result, devices_alt_result, devices_packages_sent = run_sim(base_users,
                                            devices_ref_sim, devices_alt_sim,
                                            sim_cycles)

devices_ref_diff = devices_ref_result - base_ref_result
devices_alt_diff = devices_alt_result - base_alt_result

print("One less device per router results:")
print("Ref results: ", devices_ref_result, ", difference: ", devices_ref_diff)
print("Alt results: ", devices_alt_result, ", difference: ", devices_alt_diff)
print("Packages sent: ", devices_packages_sent)
print("")


# Number of alt connections test
altcon_ref_sim = simulation(number_of_routers=base_num_routers,
                        number_of_nodes_per_router=base_num_devices_per_router)
altcon_alt_sim = simulation(number_of_routers=base_num_routers,
                        number_of_nodes_per_router=base_num_devices_per_router,
                        is_alt = True, alt_connections=base_alt_connections-1)

print("Running one less alternative connection test...")
altcon_ref_result, altcon_alt_result, altcon_packages_sent = run_sim(base_users,
                                            altcon_ref_sim, altcon_alt_sim,
                                            sim_cycles)

altcon_ref_diff = altcon_ref_result - base_ref_result
altcon_alt_diff = altcon_alt_result - base_alt_result

print("One less alternative connection results:")
print("Ref results: ", altcon_ref_result, ", difference: ", altcon_ref_diff)
print("Alt results: ", altcon_alt_result, ", difference: ", altcon_alt_diff)
print("Packages sent: ", altcon_packages_sent)
print("")
