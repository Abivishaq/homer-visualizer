import json

file1 = "/home/abivishaq/projects/Explainations_for_PA/homer-visualizer/Full_HOMER/household1/routines_train/000.json"
file3 = "/home/abivishaq/projects/Explainations_for_PA/rail_tasksim/example_graphs/CustomScene2_graph.json"


def compare_nodes(homer_nodes, sim_nodes):
    # rearrange nodes in terms of id
    print("total homer nodes:", len(homer_nodes))
    sim_node_pointer = 0
    homer_node_pointer = 0
    while homer_node_pointer < len(homer_nodes) and sim_node_pointer < len(sim_nodes):
        print(f"Comparing Homer node {homer_node_pointer} with Simulation node {sim_node_pointer}")
        
        homer_node = homer_nodes[homer_node_pointer]
        sim_node = sim_nodes[sim_node_pointer]
        print(f"Homer node: {homer_node['class_name']}, Simulation node: {sim_node['class_name']}")
        if not homer_node['class_name']==sim_node['class_name']:
            print(f"##############Node {homer_node_pointer} class name mismatch: Homer: {homer_node['class_name']}, Simulation: {sim_node['class_name']}")
            sim_node_pointer += 1
            continue
        else:
            if not homer_node['category']==sim_node['category']:
                print(f"!!!!!!!!!!!!!!!!!!!!Node {homer_node_pointer} category mismatch: Homer: {homer_node['category']}, Simulation: {sim_node['category']}")
                sim_node_pointer += 1
                continue
        homer_node_pointer += 1
        sim_node_pointer += 1
    
    if homer_node_pointer != len(homer_nodes):
        raise ValueError(f"Not all Homer nodes were matched. Remaining: {len(homer_nodes) - homer_node_pointer}")
            
    else:
        print(f"All {len(homer_nodes)} nodes matched successfully!")
        return True




homer_json = json.load(open(file1, 'r'))
homer_nodes = homer_json['graphs'][0]['nodes']


custom_json = json.load(open(file3, 'r'))
custom_nodes = custom_json['nodes']

for i in range(1,2):
    file2 = f"env_{i:02d}.json"
    sim_json = json.load(open(file2, 'r'))

    sim_nodes = sim_json['nodes']

    try:
        succ = compare_nodes(custom_nodes, sim_nodes)
        if succ:
            print(f"env_{i:02d} nodes match successfully!")
            break
    except ValueError as e:
        print(f"Error in env_{i:02d}: {e}")
        continue

# print("All nodes match successfully!")