from ortools.linear_solver import pywraplp

# Create the solver
solver = pywraplp.Solver.CreateSolver("GLOP")

# Define variables
sled_dog_trips = solver.IntVar(0, solver.infinity(), "Sled_Dog_Trips")
truck_trips = solver.IntVar(0, solver.infinity(), "Truck_Trips")

# Define the objective function: maximize the number of fish transported
objective = solver.Objective()
objective.SetCoefficient(sled_dog_trips, 100)
objective.SetCoefficient(truck_trips, 300)
objective.SetMaximization()

# Add constraints
budget_constraint = solver.Constraint(-solver.infinity(), 1000)
budget_constraint.SetCoefficient(sled_dog_trips, 50)
budget_constraint.SetCoefficient(truck_trips, 100)

sled_dog_less_than_truck_constraint = solver.Constraint(-solver.infinity(), 0)
sled_dog_less_than_truck_constraint.SetCoefficient(sled_dog_trips, 1)
sled_dog_less_than_truck_constraint.SetCoefficient(truck_trips, -1)

# Solve the problem
status = solver.Solve()

# Print the optimal solution
if status == pywraplp.Solver.OPTIMAL:
    print("Optimal Solution:")
    print("Number of sled dog trips:", sled_dog_trips.solution_value())
    print("Number of truck trips:", truck_trips.solution_value())
    print(
        "Total fish transported:",
        100 * sled_dog_trips.solution_value() + 300 * truck_trips.solution_value(),
    )
else:
    print("The problem does not have an optimal solution.")
