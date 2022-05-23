from imports.network import network_results
from imports.package import package_results
from imports.user import user, user_results
from imports.simulation import simulation
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

number_of_users = 25



users = [ user(pretty_name="User "+str(i), wait_multiplier=2000, task_rate=5)
                for i in range(number_of_users)]

for user in users:
    user.set_new_task_time()

simulation = simulation()
simulation2 = simulation()



end_of_simulation = False
while not end_of_simulation:
    for user in users:
        if user.tick():
            random_start_node = randint(len(simulation.get_devices()))
            random_goal_node = randint(len(simulation.get_devices()))
            user.create_package(simulation.get_devices()[random_start_node],
                                simulation.get_devices()[random_goal_node])
            user.set_new_task_time()

    #end_of_simulation = simulation.tick()

    if is_one_cycle:
        end_of_simulation = True

    if is_time_based and get_now() > end_time:
        end_of_simulation = True

    if not is_time_based:
        simulation_cycles -= 1
        if simulation_cycles <= 0:
            end_of_simulation = True

print(network_results(simulation.get_routers()))
print(network_results(simulation.get_devices()))
print(package_results(simulation.get_sink_packages()))
print(user_results(users))
