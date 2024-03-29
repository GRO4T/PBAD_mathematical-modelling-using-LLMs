
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

# Create a new Gurobi model
model = gp.Model("Production_Optimization")

# Decision Variables
amount = model.addVars(M, lb=0, vtype=gp.GRB.CONTINUOUS, name="amount")

# Objective Function
model.setObjective(gp.quicksum(prices[j] * amount[j] for j in range(M)), sense=gp.GRB.MAXIMIZE)

# Raw material availability constraints
for i in range(N):  # Iterate over the number of raw materials
    model.addConstr(gp.quicksum(requirements[j][i] * amount[j] for j in range(M)) <= available[i])

# Optimize the model
model.optimize()

# Extract the solution
amount_solution = [amount[j].x for j in range(M)]

# Save the output to a file
output_data = {"amount": amount_solution}
with open("output.json", "w") as outfile:
    json.dump(output_data, outfile, indent=4)
