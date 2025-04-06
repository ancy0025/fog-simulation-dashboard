import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def plot_line(results, metric):
    fig, ax = plt.subplots()
    for algo, data in results.items():
        ax.plot(range(len(data[metric])), data[metric], label=algo)
    ax.set_xlabel("Simulation Step")
    ax.set_ylabel(metric.capitalize())
    ax.legend()
    st.pyplot(fig)

def plot_radar(results):
    metrics = ["energy", "latency", "success_rate"]
    angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
    fig, ax = plt.subplots(subplot_kw={"projection": "polar"})
    for algo, data in results.items():
        values = [data[m].mean() for m in metrics]
        values += values[:1]  # Close the loop
        ax.plot(angles + angles[:1], values, label=algo)
    ax.set_xticks(angles, metrics)
    ax.legend()
    st.pyplot(fig)
