from yafs.core import Sim
from yafs.topology import Topology
from yafs.application import Application
from yafs.distribution import DeterministicDistribution
import json

def run_simulation(placement_strategy, output_file="data/results.csv"):
    # Create topology (simple star network)
    t = Topology()
    t.add_node(0, {"RAM": 4000, "CPU": 1000})  # Fog node
    t.add_node(1, {"RAM": 1000, "CPU": 200})   # Edge device
    t.add_edge(0, 1, {"BW": 100, "PR": 10})    # Link

    # Define application
    app = Application(name="SimpleApp")
    app.set_modules([{"Source": {"Type": "Sensor"}}, {"Sink": {"Type": "Actuator"}}])
    app.add_service_module("Source", 100, 10)  # CPU, RAM demand
    app.add_service_module("Sink", 50, 5)

    # Workload distribution
    dist = DeterministicDistribution(name="Deterministic", time=100)

    # Simulation
    s = Sim(t, default_results_path=output_file)
    s.deploy_app(app, placement=placement_strategy, distribution=dist)
    s.run(1000)  # Simulate for 1000 time units
    s.export_results()

if __name__ == "__main__":
    from placement_strategies import RoundRobinPlacement
    run_simulation(RoundRobinPlacement())
