from imports.user import user, user_results
from imports.simulation import simulation, simulation_results
from imports.datetime import get_now
from numpy.random import randint

k = 1000
M = k*k
G = k*M
T = k*G

is_one_cycle=False
is_time_based = False
simulation_time = 10
end_time = get_now() + simulation_time
simulation_cycles = 1000

number_of_routers = 10
number_of_nodes_per_router = 5
number_of_alt_connections = 50

number_of_users = 50
user_wait_multiplier = 2000
user_task_rate = 5



users = [ user( pretty_name="User "+str(i),
                wait_multiplier=user_wait_multiplier,
                task_rate=user_task_rate)
                for i in range(number_of_users)]

for user in users:
    user.set_new_task_time()

sim_ref = simulation(number_of_routers=number_of_routers,
                        number_of_nodes_per_router=number_of_nodes_per_router)
sim_alt = simulation(number_of_routers=number_of_routers,
                        number_of_nodes_per_router=number_of_nodes_per_router,
                        is_alt = True,
                        alt_connections=number_of_alt_connections)

simulations = [sim_ref, sim_alt]

# for device in sim1.get_devices():
#     print("ip: ", device.get_ip_address())
#
# print("------------------")
#
# for device in sim2.get_devices():
#     print("ip: ", device.get_ip_address())

# print(sim1.get_device_by_ip("0.0"))


end_of_simulation = False
while not end_of_simulation:
    for user in users:
        if user.tick():
            random_start_node = randint(len(simulations[0].get_devices()))
            random_goal_node = randint(len(simulations[0].get_devices()))

            start_node_sim1 = simulations[0].get_devices()[random_start_node]
            goal_node_sim1 = simulations[0].get_devices()[random_goal_node]
            user.create_package(start_node_sim1, goal_node_sim1)

            for i in range(1, len(simulations)):
                sim = simulations[i]
                start_node = sim.get_device_by_ip(
                                    start_node_sim1.get_ip_address())
                goal_node = sim.get_device_by_ip(
                                    goal_node_sim1.get_ip_address())
                user.create_package(start_node, goal_node)

            user.package_sent()

            user.set_new_task_time()

    for sim in simulations:
        sim.tick()

    if is_one_cycle:
        end_of_simulation = True

    if is_time_based and get_now() > end_time:
        end_of_simulation = True

    if not is_time_based:
        simulation_cycles -= 1
        if simulation_cycles <= 0:
            end_of_simulation = True



#print(simulation_results(sim_ref, "Reference"))
#print(simulation_results(sim_alt, "Alternative"))

#print(user_results(users))
