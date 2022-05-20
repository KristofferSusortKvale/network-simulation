from datetime import datetime

class simulation:
    def __init__(self):
        self.end_of_simulation = False
        self.package_count = 0

    def get_new_file_name(self):
        self.package_count += 1
        return "package" + str(self.package_count) + ".json"

    def end_simulation(self):
        self.end_of_simulation = True

simulation_time = 30
sim = simulation()
simulation_start = datetime.now()

while int(datetime.now() - simulation_start) < simulation_time:
    
