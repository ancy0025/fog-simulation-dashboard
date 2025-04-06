from yafs.placement import Placement
import random

# Traditional: Round Robin
class RoundRobinPlacement(Placement):
    def __init__(self):
        self.current = 0
        self.name = "RoundRobin"

    def place(self, sim, app_name, service):
        nodes = sim.topology.G.nodes()
        node = list(nodes)[self.current % len(nodes)]
        self.current += 1
        return {service: node}

# Metaheuristic: Arithmetic Optimization Algorithm (simplified)
class AOAPlacement(Placement):
    def __init__(self):
        self.name = "AOA"

    def place(self, sim, app_name, service):
        nodes = list(sim.topology.G.nodes())
        # Simplified AOA: Optimize based on node CPU capacity
        best_node = max(nodes, key=lambda n: sim.topology.G.nodes[n]["CPU"])
        return {service: best_node}

# Add more: GA, PSO, RL, etc., as needed
