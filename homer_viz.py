import json
import os
from virtualhome.virtualhome.simulation.unity_simulator import comm_unity
from virtualhome.virtualhome.simulation.evolving_graph.environment import EnvironmentGraph, EnvironmentState
import time

import subprocess

# Start the Unity simulator
start_simulator = True
if start_simulator:
    sim_exe = "/home/abivishaq/projects/Explainations_for_PA/homer-visualizer/virtualhome/virtualhome/simulation/linux_exec.v2.3.0.x86_64"
    subprocess.Popen([sim_exe])
    time.sleep(5)  # Wait for the simulator to start
    print("Simulator started successfully.")


CustomScene2_graph = "/home/abivishaq/projects/Explainations_for_PA/rail_tasksim/example_graphs/CustomScene2_graph.json"
with open(CustomScene2_graph, 'r') as f:
    custom_scene_graph = json.load(f)


class HomerViz:
    def __init__(self, household_id = 0, train_set = True, dataset_path=None):
        """
        Initializes the HomerViz class with the dataset path, household ID, and day ID.
        :param dataset_path: Path to the dataset directory.
        :param
        household_id: ID of the household to visualize.
        :param day_id: ID of the day to visualize.
        :param train_set: Boolean indicating if the dataset is a training set or test set.
        """
        self.dataset_path = dataset_path
        if dataset_path is None:
            self.dataset_path = '/home/abivishaq/projects/Explainations_for_PA/homer-visualizer/Full_HOMER'
        
        self.household_id = household_id
        self.day_id = day_id
        self.train_set = train_set

        self.json_folder = 'raw_routines_train' if train_set else 'raw_routines_test'
        self.json_folder_path = f"{self.dataset_path}/household{household_id}/{self.json_folder}"

        env_graph = EnvironmentGraph(custom_scene_graph)
        env_state = EnvironmentState(env_graph, name_equivalence={})  # empty dict is OK for no aliasing

        self.comm = comm_unity.UnityCommunication()
        self.comm.reset(0)  # Reset base env first

        # # Then expand the environment to match your scene graph
        # success, message = self.comm.expand_scene(env_state.to_dict())
        # if not success:
        #     raise RuntimeError(f"Scene expansion failed: {message}")
        # print("Scene initialized with custom environment graph.")


        

    def visualize_day(self, day_id):
        """
        Visualizes the routines for a specific day.
        :param day_id: ID of the day to visualize.
        """
        self.day_id = day_id
        json_file_path = f"{self.json_folder_path}/{int(day_id):03d}.json"
        
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        
        print(data.keys())

        graph_homer = data['graphs'][0]

        # self.comm.reset(0)
        success, image = self.comm.camera_image([0])
        print("Image received from the simulator:", success)
        if not success:
            print("Failed to receive image from the simulator.")
            return
        # print("Image",image)

        for i in range(20):
            self.comm.reset(i)
            success, graph = self.comm.environment_graph()
            success, image = self.comm.camera_image([0])
            if success:
                with open(f"env_{i:02d}.json", "w") as f:
                    json.dump(graph, f, indent=4)
            else:
                print(f"Failed to get environment graph for env {i:02d}")
        success, graph_sim = self.comm.environment_graph()
        print("graph sim", type(graph_sim), graph_sim.keys())

        #save graph sim to json
        graph_sim_path = "graph_sim.json"
        with open(graph_sim_path, 'w') as f:
            json.dump(graph_sim, f, indent=4)
        print("Graph sim saved to", graph_sim_path)


        


if __name__ == "__main__":
    # Example usage
    household_id = 0
    day_id = 1
    train_set = True

    homer_viz = HomerViz(household_id, train_set)
    homer_viz.visualize_day(day_id)
    
        