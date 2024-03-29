
import gurobipy as gp
import json

# Read data from the input file
with open("data.json", "r") as file:
    data = json.load(file)

C = data["C"]
values = data["value"]
sizes = data["size"]
K = len(values)

# Create a new model
model = gp.Model()

# Decision Variables
x = model.addVars(K, vtype=gp.GRB.BINARY, name="x")

# Objective Function
model.setObjective(sum(values[k] * x[k] for k in range(K)), sense=gp.GRB.MAXIMIZE)

# Capacity Constraint
model.addConstr(sum(sizes[k] * x[k] for k in range(K)) <= C)

# Optimize the model
model.optimize()

# Retrieve the solution
solution = [x[k].x for k in range(K)]

# Save the output to a file
output_data = {"isincluded": solution}
with open("output.json", "w") as output_file:
    json.dump(output_data, output_file, indent=4)
