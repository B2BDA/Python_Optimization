markdown_table = """
| Type   | Sales Price $ | Cost $ | Labor (hours) | Cloth (sq yd) |
|--------|---------------|--------|---------------|---------------|
| Shirt  | 12            | 6      | 3             | 4             |
| Shorts | 8             | 4      | 2             | 3             |
| Pants  | 15            | 8      | 6             | 4             |
"""

print(markdown_table)

import pyomo.environ as pyo
from pyomo.opt import SolverFactory

#Define the model
model = pyo.ConcreteModel()

# Define the sets
model.i = pyo.Set(initialize=['Shirt', 'Shorts', 'Pants'])
# Define the parameters
model.SalesPrice = pyo.Param(model.i, initialize={'Shirt': 12, 'Shorts': 8, 'Pants': 15})
model.Cost = pyo.Param(model.i, initialize={'Shirt': 6, 'Shorts': 4, 'Pants': 8})
model.Labor = pyo.Param(model.i, initialize={'Shirt': 3, 'Shorts': 2, 'Pants': 6})
model.Cloth = pyo.Param(model.i, initialize={'Shirt': 4, 'Shorts': 3, 'Pants': 4})
model.Machine_Rent = pyo.Param(model.i, initialize={'Shirt': 200, 'Shorts': 150, 'Pants': 100})
model.M = pyo.Param(model.i, initialize={'Shirt': 40, 'Shorts': 53, 'Pants': 25})

# Define the decision variables
model.x = pyo.Var(model.i, within=pyo.Integers)
model.y = pyo.Var(model.i, within=pyo.Binary)
# Define the objective function
def objective_rule(model):
    return sum(model.SalesPrice[i]* model.x[i]  for i in model.i) -\
          sum(model.Cost[i]* model.x[i] for i in model.i) - \
            sum(model.Machine_Rent[i]* model.y[i] for i in model.i )

model.obj = pyo.Objective(rule=objective_rule, sense=pyo.maximize)
# Define the constraints   

def LaborConstraint(model, i):
    return sum(model.Labor[i] * model.x[i] for i in model.i) <= 150
model.LaborConstraint = pyo.Constraint(model.i, rule=LaborConstraint)

def ClothConstraint(model, i):
    return sum(model.Cloth[i] * model.x[i] for i in model.i) <= 160
model.ClothConstraint = pyo.Constraint(model.i, rule=ClothConstraint)



def constraint_m(model, i):
    return model.x[i] <= model.M[i] * model.y[i]
model.M_Constraint = pyo.Constraint(model.i, rule=constraint_m)

# Solve the model
optm = SolverFactory('cplex_direct')
results = optm.solve(model)
print(results)
# Display the results
print("Objective value:", pyo.value(model.obj))
print("Shirt value:", pyo.value(model.x['Shirt']))
print("Shorts value:", pyo.value(model.x['Shorts']))
print("Pants value:", pyo.value(model.x['Pants'])) 
