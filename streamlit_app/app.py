import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import subprocess

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
    try:
        # Get absolute paths
        base_dir = Path(__file__).parent.parent
        sim_script = base_dir / "yafs_sim" / "simulation.py"
        
        # Run simulation
        cmd = f"python {sim_script} --strategy {strategy} --nodes {nodes} --tasks {tasks}"
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        
        st.success("✅ Simulation Completed!")
        
        # Show results
        result_path = base_dir / "data" / "results.csv"
        if result_path.exists():
            df = pd.read_csv(result_path)
            st.subheader("📊 Comparative Metrics")
            
            st.dataframe(df.sort_values(by="Latency"))
            
            fig, ax = plt.subplots()
            df.plot(x="Strategy", y=["Latency", "Energy"], ax=ax, kind="line")
            st.pyplot(fig)
        else:
            st.warning("No results file found.")
            
    except subprocess.CalledProcessError as e:
        st.error(f"❌ Simulation failed: {e.stderr}")
    except Exception as e:
        st.error(f"⚠️ Unexpected error: {str(e)}")
