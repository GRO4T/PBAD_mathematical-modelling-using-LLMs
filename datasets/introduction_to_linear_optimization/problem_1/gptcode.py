
import gurobipy as gp
import json

# Read data from the input file
with open("data.json", "r") as file:
    data = json.load(file)

available = data["available"]
requirements = data["requirements"]
prices = data["prices"]
M = len(prices)
N = len(available)

# Create a new model
model = gp.Model("production_optimization")

# Decision variables
x = {}
for j in range(M):
    x[j] = model.addVar(lb=0, vtype=gp.GRB.CONTINUOUS, name=f"x_{j}")

# Update model to integrate new variables
model.update()

# Set objective function
model.setObjective(gp.quicksum(prices[j] * x[j] for j in range(M)), sense=gp.GRB.MAXIMIZE)

# Add constraints
for i in range(N):
    model.addConstr(gp.quicksum(requirements[j][i] * x[j] for j in range(M)) <= available[i], name=f"raw_material_{i}")

# Optimize the model
model.optimize()

# Extract the solution
amount = [x[j].x for j in range(M)]

# Save the output to a file
output = {"amount": amount}
with open("output.json", "w") as file:
    json.dump(output, file, indent=4)
