import pandas as pd

def compute_metrics(csv_path="data/results.csv"):
    df = pd.read_csv(csv_path)
    energy = df["energy"].sum() if "energy" in df else 0  # Placeholder
    latency = df["time_in"] - df["time_out"] if "time_in" in df else df["time"].mean()
    success_rate = (df["success"].sum() / len(df)) * 100 if "success" in df else 100
    return {"energy": energy, "latency": latency.mean(), "success_rate": success_rate}
