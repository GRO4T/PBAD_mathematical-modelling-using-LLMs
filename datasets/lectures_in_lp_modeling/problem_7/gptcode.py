
import json
import gurobipy as gp

# Read data from the input file
with open("data.json", "r") as file:
    data = json.load(file)

demand = data["demand"]
max_regular_amount = data["max_regular_amount"]
cost_regular = data["cost_regular"]
cost_overtime = data["cost_overtime"]
store_cost = data["store_cost"]
N = len(demand)

# Create a new optimization model
model = gp.Model("production_schedule")

# Decision Variables
reg_quant = model.addVars(N, name="reg_quant")
over_quant = model.addVars(N, name="over_quant")

# Objective Function
model.setObjective(
    gp.quicksum(cost_regular * reg_quant[n] + cost_overtime * over_quant[n] + store_cost * gp.quicksum(reg_quant[i] + over_quant[i] - demand[i] for i in range(n+1)) for n in range(N),
    sense=gp.GRB.MINIMIZE)

# Demand Constraint
demand_constraint = model.addConstrs(reg_quant[n] + over_quant[n] >= demand[n] for n in range(N))

# Regular Production Limit Constraint
regular_limit_constraint = model.addConstrs(reg_quant[n] <= max_regular_amount for n in range(N))

# Solve the optimization problem
model.optimize()

# Extract the optimal production quantities
reg_quant_values = [reg_quant[n].x for n in range(N)]
over_quant_values = [over_quant[n].x for n in range(N)]

# Save the output to a file
output_data = {
    "reg_quant": reg_quant_values,
    "over_quant": over_quant_values
}

with open("output.json", "w") as output_file:
    json.dump(output_data, output_file, indent=4)
