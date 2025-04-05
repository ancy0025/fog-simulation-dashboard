# simulation.py

from yafs.core import Sim
from yafs.population import Population
from yafs.topology import Topology
from yafs.placement import Placement
from yafs.application import Application

from pathlib import Path
import random
import csv
import os
import time

def run_simulation(strategy="FCFS", num_nodes=5, num_tasks=20):
    print(f"Running simulation with strategy: {strategy}, nodes: {num_nodes}, tasks: {num_tasks}")

    results_dir = Path.cwd() / "data"
    results_dir.mkdir(parents=True, exist_ok=True)
    csv_path = results_dir / "results.csv"
    if not csv_path.exists():
        with open(csv_path, "w") as f:
            pass  # create empty file

    # Create topology
    topo = Topology()
    topo_json = {
        "entity": [{"id": i, "model": "fog_node", "RAM": 4000} for i in range(num_nodes)],
        "link": [{"s": i, "d": i+1, "BW": 1, "PR": 1} for i in range(num_nodes-1)]
    }
    topo.load(topo_json)

    # Application
    app = Application(name="SimpleApp")
    app.set_modules([{"SimpleModule": {"RAM": 100}}])
    app.set_message("M1", "SimpleModule", "SimpleModule", instructions=100, bytes=100)
    app.add_source_messages("M1")

    # Placement
    placement = Placement(name="placement")
    if strategy == "FCFS":
        placement.set_module_placement("SimpleModule", [0])
    elif strategy == "RoundRobin":
        placement.set_module_placement("SimpleModule", [i % num_nodes for i in range(num_tasks)])
    elif strategy == "SJF":
        placement.set_module_placement("SimpleModule", sorted(range(num_nodes)))
    elif strategy == "LJF":
        placement.set_module_placement("SimpleModule", sorted(range(num_nodes), reverse=True))
    elif strategy == "MinMin":
        placement.set_module_placement("SimpleModule", [0] * num_tasks)
    elif strategy == "MaxMin":
        placement.set_module_placement("SimpleModule", [num_nodes-1] * num_tasks)
    elif strategy == "Greedy":
        placement.set_module_placement("SimpleModule", [random.randint(0, num_nodes-1) for _ in range(num_tasks)])
    else:  # For all advanced strategies
        placement.set_module_placement("SimpleModule", [random.choice(range(num_nodes)) for _ in range(num_tasks)])

    # Population
    pop = Population(name="FogUsers")
    pop.set_src_nodes([0])
    pop.set_sink_modules(["SimpleModule"])

    # Simulation
    sim = Sim(topo, default_results_path=str(results_dir))
    sim.deploy_app(app, placement, pop)
    start = time.time()
    sim.run(100)
    end = time.time()

    # Placeholder metrics
    latency = random.uniform(5.0, 15.0)
    energy = random.uniform(20.0, 50.0)

    with open(csv_path, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if os.stat(csv_path).st_size == 0:
            writer.writerow(["Strategy", "Nodes", "Tasks", "Latency", "Energy", "Runtime"])
        writer.writerow([strategy, num_nodes, num_tasks, round(latency, 2), round(energy, 2), round(end - start, 2)])

    print("Simulation finished.")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--strategy", default="FCFS")
    parser.add_argument("--nodes", type=int, default=5)
    parser.add_argument("--tasks", type=int, default=20)
    args = parser.parse_args()
    run_simulation(args.strategy, args.nodes, args.tasks)
