from yafs.core import Sim
from yafs.topology import Topology
from yafs.application import Application
from yafs.distribution import deterministic_distribution
import json

def run_simulation(placement_strategy, output_file="data/results.csv"):
    t = Topology()
    t.add_node(id=0, RAM=4000, CPU=1000)  # Use keyword arguments
    t.add_node(id=1, RAM=1000, CPU=200)
    t.add_edge(0, 1, BW=100, PR=10)

    app = Application(name="SimpleApp")
    app.set_modules([{"Source": {"Type": "Sensor"}}, {"Sink": {"Type": "Actuator"}}])
    app.add_service_module("Source", 100, 10)
    app.add_service_module("Sink", 50, 5)

    dist = deterministic_distribution(name="Deterministic", time=100)

    s = Sim(t, default_results_path=output_file)
    s.deploy_app(app, placement=placement_strategy, distribution=dist)
    s.run(1000)
    s.export_results()

if __name__ == "__main__":
    from placement_strategies import RoundRobinPlacement
    run_simulation(RoundRobinPlacement())
