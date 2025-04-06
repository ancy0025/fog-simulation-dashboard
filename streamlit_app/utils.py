from yafs_sim.metrics import compute_metrics

def load_results(csv_path):
    return compute_metrics(csv_path)
