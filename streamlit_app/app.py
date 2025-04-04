import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.title("⚙️ Fog Computing Simulator Dashboard")

strategies = [
    "FCFS", "RoundRobin", "SJF", "LJF", "MinMin", "MaxMin", "Greedy",
    "GA", "PSO", "ACO", "Firefly", "Bat", "ABC", "AOA",
    "Hybrid-GA+ACO", "Hybrid-GA+PSO", "Fuzzy+SA",
    "ML", "RL", "DeepRL", "DQN",
    "GreenCloud", "DigitalTwin", "FederatedLearning", "XAI",
    "Blockchain", "Quantum"
]

strategy = st.selectbox("Select Scheduling Strategy", strategies)
nodes = st.slider("Number of Nodes", 2, 20, 5)
tasks = st.slider("Number of Tasks", 10, 100, 20)

if st.button("▶️ Run Simulation"):
    os.system(f"python ..fog-simulation-dashboard/yafs_sim/simulation.py --strategy {strategy} --nodes {nodes} --tasks {tasks}")
    st.success("Simulation Completed!")

    result_path = "..fog-simulation-dashboard/data/results.csv"
    if os.path.exists(result_path):
        df = pd.read_csv(result_path)
        st.subheader("📊 Comparative Metrics")

        st.dataframe(df.sort_values(by="Latency"))

        st.line_chart(df.set_index("Strategy")["Latency"], use_container_width=True)
        st.line_chart(df.set_index("Strategy")["Energy"], use_container_width=True)
        st.line_chart(df.set_index("Strategy")["Runtime"], use_container_width=True)
    else:
        st.warning("No results file found. Please check simulation output.")

