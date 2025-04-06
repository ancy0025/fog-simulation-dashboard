import streamlit as st
from yafs_sim.simulation import run_simulation
from yafs_sim.placement_strategies import RoundRobinPlacement, AOAPlacement  # Adjust as needed
from streamlit_app.utils import load_results  # Import the function

st.title("Fog Simulation Dashboard")

algos = {
    "Round Robin": RoundRobinPlacement,
    "AOA": AOAPlacement  # Add your algorithms here
}

selected_algos = st.multiselect("Select Algorithms", list(algos.keys()))

# Run simulations
if st.button("Run Simulations"):
    for algo_name in selected_algos:
        run_simulation(algos[algo_name](), output_file=f"data/results_{algo_name}.csv")
    st.success("Simulations completed!")

# Load and display results
results = {algo: load_results(f"data/results_{algo}.csv") for algo in selected_algos}
metric = st.selectbox("Select Metric", ["energy", "latency", "success_rate"])  # Adjust metrics as needed

# Visualizations (add your plotting code here)
if results:
    st.write("Results loaded:", results)
