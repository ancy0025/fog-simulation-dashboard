import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import yafs

st.write("YAFS Path:", yafs.__file__)
st.write("YAFS Modules:", dir(yafs))

from yafs_sim.simulation import run_simulation
from yafs_sim.placement_strategies import RoundRobinPlacement, AOAPlacement

st.title("Fog Simulation Dashboard")

# Sidebar: Select algorithms
algos = {"Round Robin": RoundRobinPlacement, "AOA": AOAPlacement}
selected_algos = st.sidebar.multiselect("Select Algorithms", list(algos.keys()))

# Run simulations
if st.button("Run Simulations"):
    for algo_name in selected_algos:
        run_simulation(algos[algo_name](), output_file=f"data/results_{algo_name}.csv")
    st.success("Simulations completed!")

# Load and display results
results = {algo: load_results(f"data/results_{algo}.csv") for algo in selected_algos}
metric = st.selectbox("Select Metric", ["energy", "latency", "success_rate"])

# Visualizations
if results:
    plot_line(results, metric)
    plot_radar(results)
