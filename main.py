from imports.network import network_results
from imports.simulation import simulation

k = 1000
M = k*k
G = k*M
T = k*G

simulation = simulation()

end_of_simulation = False
while not end_of_simulation:
    end_of_simulation = simulation.tick()

network_results(simulation.get_nodes())
