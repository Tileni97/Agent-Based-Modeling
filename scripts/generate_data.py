import pandas as pd
import numpy as np
import os

# Create the 'data' folder if it doesn't exist
data_folder = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(data_folder, exist_ok=True)

# Artists
artists = pd.DataFrame(
    {
        "Artist_ID": range(1, 101),
        "Project_Size": np.random.choice(["small", "medium", "large"], 100),
        "Urgency": np.random.choice(["low", "medium", "high"], 100),
    }
)

# Nodes
nodes = pd.DataFrame(
    {
        "Node_ID": range(1, 21),
        "Pricing_Tier": np.random.choice(["low", "medium", "high"], 20),
        "Bandwidth": np.random.randint(10, 100, 20),
        "Availability": np.random.uniform(0.5, 1.0, 20),  # 50-100% availability
    }
)

# Jobs (to be populated during simulation)
jobs = pd.DataFrame(
    columns=["Job_ID", "Artist_ID", "Node_ID", "Completion_Time", "Cost"]
)

# Save data
artists.to_csv(os.path.join(data_folder, "artists.csv"), index=False)
nodes.to_csv(os.path.join(data_folder, "nodes.csv"), index=False)
jobs.to_csv(os.path.join(data_folder, "jobs.csv"), index=False)

print("Synthetic data generated and saved to the 'data' folder.")
