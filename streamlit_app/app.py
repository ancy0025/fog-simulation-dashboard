# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import subprocess
import os

st.set_page_config(page_title="Fog Simulator", layout="wide")
st.title("⚙️ Fog Computing Simulator Dashboard")

# Scheduling strategies
strategies = [
    "FCFS", "RoundRobin", "SJF", "LJF", "MinMin", "MaxMin", "Greedy",
    "GA", "PSO", "ACO", "Firefly", "Bat", "ABC", "AOA",
    "Hybrid-GA+ACO", "Hybrid-GA+PSO", "Fuzzy+SA",
    "ML", "RL", "DeepRL", "DQN",
    "GreenCloud", "DigitalTwin", "FederatedLearning", "XAI",
    "Blockchain", "Quantum"
]

# UI Inputs
strategy = st.selectbox("📌 Select Scheduling Strategy", strategies)
nodes = st.slider("🖧 Number of Nodes", 2, 20, 5)
tasks = st.slider("🧮 Number of Tasks", 10, 100, 20)

if st.button("▶️ Run Simulation"):
    with st.spinner("Running simulation..."):
        try:
            # Set paths
            base_dir = Path.cwd()
            sim_script = base_dir / "yafs_sim" / "simulation.py"
            results_dir = base_dir / "data"
            results_dir.mkdir(exist_ok=True)

            # Run the simulation
            cmd = f"python {str(sim_script)} --strategy {strategy} --nodes {nodes} --tasks {tasks}"
            result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)

            st.success("✅ Simulation Completed!")
            st.code(result.stdout)

            # Show results
            result_path = results_dir / "results.csv"
            if result_path.exists():
                df = pd.read_csv(result_path)
                st.subheader("📊 Comparative Metrics")
                st.dataframe(df.sort_values(by="Latency"))

                fig, ax = plt.subplots()
                df.plot(x="Strategy", y=["Latency", "Energy"], ax=ax, kind="bar")
                st.pyplot(fig)
            else:
                st.warning("⚠️ No results found.")
        except subprocess.CalledProcessError as e:
            st.error(f"❌ Simulation failed:\n{e.stderr}")
        except Exception as e:
            st.error(f"⚠️ Unexpected error:\n{str(e)}")
