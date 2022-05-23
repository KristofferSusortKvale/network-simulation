from imports.network import network_results
from imports.package import package_results
from imports.user import user, user_results
from imports.simulation import simulation
from numpy.random import randint

k = 1000
M = k*k
G = k*M
T = k*G

number_of_users = 25
users = [ user(pretty_name="User "+str(i), wait_multiplier=2000, task_rate=5)
                for i in range(number_of_users)]

for user in users:
    user.set_new_task_time()

simulation = simulation(users)



end_of_simulation = False
while not end_of_simulation:
    for user in users:
        if user.tick():
            random_start_node = randint(len(simulation.get_devices()))
            random_goal_node = randint(len(simulation.get_devices()))
            user.create_package(simulation.get_devices()[random_start_node],
                                simulation.get_devices()[random_goal_node])
            user.set_new_task_time()

    end_of_simulation = simulation.tick()

print(network_results(simulation.get_routers()))
print(network_results(simulation.get_devices()))
print(package_results(simulation.get_sink_packages()))
print(user_results(simulation.get_users()))
