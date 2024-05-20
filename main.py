from simulation.computers import Server, Station, Resolution
from visulisation.visual import Visualization
from simulation.sim import Simulation
import random

sim = Simulation()

for i in range(random.randint(2, 5)):
    sim.add_server(Server(random.uniform(0.000001, 0.0001), bool(random.randbytes(1)), bool(random.randbytes(1)), bool(random.randbytes(1))))

for i in range(random.randint(2, 4)):
    room = sim.create_room(random.choices(sim.servers, k=random.randint(2, len(sim.servers))))
    for j in range(2, 9):
        sim.add_station(Station(random.uniform(0.0005, 0.001), random.choice((Resolution.HD, Resolution.UltraHD, Resolution.FullHD)), room))

Visualization(sim, 800, 500)
