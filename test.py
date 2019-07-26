import numpy as np

a = [(0, 1), (2, 3)]
arr = np.array(a)
print(range(len(arr)))
indices = np.random.choice(range(len(arr)), 5)
print(indices)
print(arr[indices])