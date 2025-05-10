import pyomo.environ as pyo
from pyomo.opt import SolverFactory


######### Problem 1 #########

# Define the model
model = pyo.ConcreteModel()

# Define the decision variables
model.x1 = pyo.Var(within=pyo.NonNegativeReals)
model.x2 = pyo.Var(within=pyo.NonNegativeReals)
# Define the objective function
model.obj = pyo.Objective(expr=4 * model.x1 + 3 * model.x2, sense=pyo.maximize)
# Define the constraints
model.con1 = pyo.Constraint(expr=2 * model.x1 + model.x2 <= 60)
model.con2 = pyo.Constraint(expr=model.x1 + model.x2 <= 40)

optm = SolverFactory('glpk')
results = optm.solve(model)

print(results)

print("Objective value:", pyo.value(model.obj))
print("x1 value:", pyo.value(model.x1))
print("x2 value:", pyo.value(model.x2))


######### Problem 2 #########

table_string = """
| Resource          | Desk | Table | Chair |
|-------------------|------|-------|-------|
| Lumber (ft)       | 8    | 6     | 1     |
| Finishing hours   | 4    | 2     | 1.5   |
| Carpentry hours   | 2    | 1.5   | 0.5   |
"""

print(table_string)

# Define the model
model2 = pyo.ConcreteModel()

# Define the sets
model2.i = pyo.Set(initialize=['Desk', 'Table', 'Chair'])

# Define the parameters
model2.Lumber = pyo.Param(model2.i, initialize={'Desk': 8, 'Table': 6, 'Chair': 1})
model2.Finishing = pyo.Param(model2.i, initialize={'Desk': 4, 'Table': 2, 'Chair': 1.5})
model2.Carpentry = pyo.Param(model2.i, initialize={'Desk': 2, 'Table': 1.5, 'Chair': 0.5})
model2.Profit = pyo.Param(model2.i, initialize={'Desk': 60, 'Table': 30, 'Chair': 20})

# Define the decision variables
model2.x = pyo.Var(model2.i, within=pyo.NonNegativeReals)

# Define the objective function

def objective_rule(model2):
    return sum(model2.Profit[i] * model2.x[i] for i in model2.i)

model2.obj = pyo.Objective(rule=objective_rule, sense=pyo.maximize)
# Define the constraints
def lumber_constraint_rule(model,i):
    return sum(model.Lumber[i] * model.x[i] for i in model.i) <= 48

model2.lumber_constraint = pyo.Constraint(model2.i, rule=lumber_constraint_rule)

def finishing_constraint_rule(model,i):
    return sum(model.Finishing[i] * model.x[i] for i in model.i) <= 20

model2.finishing_constraint_rule = pyo.Constraint(model2.i, rule=finishing_constraint_rule)

def carpentry_constraint_rule(model,i):
    return sum(model.Carpentry[i] * model.x[i] for i in model.i) <= 8

model2.carpentry_constraint_rule = pyo.Constraint(model2.i, rule=carpentry_constraint_rule)

def table_constraint_rule(model,i):
    return model.x['Table'] <= 5

model2.table_constraint_rule = pyo.Constraint(model2.i, rule=table_constraint_rule)

#Solve the model
Solver = SolverFactory('glpk')
results2 = Solver.solve(model2)
print(results2)
print("Objective value:", pyo.value(model2.obj()))
for i in model2.i:
    print(f"{i} value:", pyo.value(model2.x[i]))

# # Define the decision variables
# model2.t = pyo.Var(within=pyo.NonNegativeReals)
# model2.d = pyo.Var(within=pyo.NonNegativeReals)
# model2.c = pyo.Var(within=pyo.NonNegativeReals)
# # Define the objective function
# model2.obj = pyo.Objective(expr=60*model2.d + 30 * model2.t + 20 * model2.c, sense=pyo.maximize)
# # Define the constraints
# model2.con1 = pyo.Constraint(expr= 8 * model2.d + 6 * model2.t + model2.c <= 48)
# model2.con2 = pyo.Constraint(expr= 4 * model2.d + 2 * model2.t + 1.5*model2.c <= 20)
# model2.con3 = pyo.Constraint(expr= 2 * model2.d + 1.5 * model2.t + 0.5*model2.c <= 8)
# model2.con4 = pyo.Constraint(expr= model2.t <= 5)

# optm2 = SolverFactory('glpk')
# results2 = optm2.solve(model2)  
# print(results2)
# print("Objective value:", pyo.value(model2.obj))
# print("d value:", pyo.value(model2.d))
# print("t value:", pyo.value(model2.t))
# print("c value:", pyo.value(model2.c))

#### Problem 3 #####

# Transportation Problem Data:
#
# From     | To City1 | To City2 | To City3 | To City4 | Supply (Million kWh)
# ---------|----------|----------|----------|----------|--------------------
# Plant1   | $8       | $6       | $10      | $9       | 35
# Plant2   | $9       | $12      | $13      | $7       | 50
# Plant3   | $14      | $9       | $16      | $5       | 40
# ---------|----------|----------|----------|----------|--------------------
# Demand   | 45       | 20       | 30       | 30       |
# (Million kWh)

# Define the model
model3 = pyo.ConcreteModel()
# Define the sets
model3.i = pyo.Set(initialize=['Plant1', 'Plant2', 'Plant3'])
model3.j = pyo.Set(initialize=['City1', 'City2', 'City3', 'City4'])
# Define the parameters
model3.cost = pyo.Param(model3.i, model3.j, initialize={
    ('Plant1', 'City1'): 8,
    ('Plant1', 'City2'): 6,
    ('Plant1', 'City3'): 10,
    ('Plant1', 'City4'): 9,
    ('Plant2', 'City1'): 9,
    ('Plant2', 'City2'): 12,
    ('Plant2', 'City3'): 13,
    ('Plant2', 'City4'): 7,
    ('Plant3', 'City1'): 14,
    ('Plant3', 'City2'): 9,
    ('Plant3', 'City3'): 16,
    ('Plant3', 'City4'): 5
})

model3.supply = pyo.Param(model3.i, initialize={
    'Plant1': 35,
    'Plant2': 50,
    'Plant3': 40
})
model3.demand = pyo.Param(model3.j, initialize={
    'City1': 45,
    'City2': 20,
    'City3': 30,
    'City4': 30
})

# Define the decision variables
model3.x = pyo.Var(model3.i, model3.j, within=pyo.NonNegativeReals)
# Define the objective function
def objective_rule(model3):
    return sum(model3.cost[i, j] * model3.x[i, j] for i in model3.i for j in model3.j)  
model3.obj = pyo.Objective(rule=objective_rule, sense=pyo.minimize)

# Define the constraints
def supply_constraint_rule(model3, i):
    return sum(model3.x[i, j] for j in model3.j) <= model3.supply[i]
model3.supply_constraint = pyo.Constraint(model3.i, rule=supply_constraint_rule)
def demand_constraint_rule(model3, j):
    return sum(model3.x[i, j] for i in model3.i) >= model3.demand[j]
model3.demand_constraint = pyo.Constraint(model3.j, rule=demand_constraint_rule)
# Solve the model   
Solver = SolverFactory('glpk')
results3 = Solver.solve(model3)
print(results3)
print("Objective value:", pyo.value(model3.obj))
for i in model3.i:
    for j in model3.j:
        print(f"From {i} to {j}: {pyo.value(model3.x[i, j])} million kWh")

        