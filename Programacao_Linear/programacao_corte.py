from pulp import LpVariable, LpProblem, lpSum, LpStatus, LpMinimize, value
import numpy as np

# Problem data
orders = np.array([1, 2, 3])
dimensions = [[0.40, 10],
              [0.60, 30],
              [0.70, 20]]

plate_1 = [[2, 0, 0],
           [0, 1, 0],
           [0, 1, 1]]

plate_2 = [[3, 2, 2, 1, 0, 0],
           [0, 1, 0, 1, 1, 0],
           [0, 0, 1, 0, 1, 2]]

loss_trim = np.array([0, 0.4, 0.3, 0.3, 0.1, 0, 0.5, 0.2, 0.1])

required_length = np.array([10, 30, 20])
