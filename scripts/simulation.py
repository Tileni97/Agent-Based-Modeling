from mesa import Agent
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import numpy as np
import pandas as pd


class Artist(Agent):
    def __init__(self, unique_id, model, project_size, urgency):
        super().__init__(unique_id, model)
        self.project_size = project_size
        self.urgency = urgency
        self.job_completed = False

    def submit_job(self):
        if not self.job_completed:
            available_nodes = [
                node
                for node in self.model.schedule.agents
                if isinstance(node, Node) and node.is_available()
            ]
            if available_nodes:
                chosen_node = np.random.choice(available_nodes)
                chosen_node.assign_job(self)
                self.job_completed = True

    def step(self):
        self.submit_job()


class Node(Agent):
    def __init__(self, unique_id, model, pricing_tier, bandwidth, availability):
        super().__init__(unique_id, model)
        self.pricing_tier = pricing_tier
        self.bandwidth = bandwidth
        self.availability = availability
        self.current_job = None
        self.completion_time = 0  # Track completion time

    def is_available(self):
        return self.current_job is None and np.random.random() < self.availability

    def assign_job(self, artist):
        if self.is_available():
            self.current_job = artist
            size_factor = {"small": 1, "medium": 2, "large": 3}[artist.project_size]
            self.completion_time = size_factor * (
                100 / self.bandwidth
            )  # Simulate processing time
            self.model.jobs.append(
                {
                    "Job_ID": len(self.model.jobs) + 1,
                    "Artist_ID": artist.unique_id,
                    "Node_ID": self.unique_id,
                    "Completion_Time": self.completion_time,
                    "Cost": size_factor
                    * {"low": 10, "medium": 20, "high": 30}[self.pricing_tier],
                }
            )

    def step(self):
        if self.current_job:
            self.completion_time -= 1
            if self.completion_time <= 0:
                self.current_job = None  # Job completed


class RenderNetwork(Model):
    def __init__(self, num_artists, num_nodes):
        self.num_artists = num_artists
        self.num_nodes = num_nodes
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(10, 10, True)
        self.jobs = []
        self.datacollector = DataCollector(
            agent_reporters={
                "Jobs_Completed": lambda a: (
                    1 if isinstance(a, Artist) and a.job_completed else 0
                )
            }
        )

        # Create artists
        for i in range(self.num_artists):
            project_size = np.random.choice(["small", "medium", "large"])
            urgency = np.random.choice(["low", "medium", "high"])
            artist = Artist(i, self, project_size, urgency)
            self.schedule.add(artist)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(artist, (x, y))

        # Create nodes
        for i in range(self.num_artists, self.num_artists + self.num_nodes):
            pricing_tier = np.random.choice(["low", "medium", "high"])
            bandwidth = np.random.randint(10, 100)
            availability = np.random.uniform(0.5, 1.0)
            node = Node(i, self, pricing_tier, bandwidth, availability)
            self.schedule.add(node)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(node, (x, y))

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()


if __name__ == "__main__":
    model = RenderNetwork(num_artists=100, num_nodes=20)
    for i in range(50):  # Simulate 50 steps
        model.step()

    # Save results
    jobs_df = pd.DataFrame(model.jobs)
    jobs_df.to_csv(
        "C:/Users/Chang/OneDrive/Desktop/Data Analysis/Agent-Based-Modeling/data/jobs.csv",
        index=False,
    )
    print("Simulation complete. Job data saved to 'data/jobs.csv'.")
