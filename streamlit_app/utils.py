import pandas as pd

def load_results(file_path):
    """Load simulation results from a CSV file."""
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        return pd.DataFrame()  # Return empty DataFrame if file is missing
