import numpy as np

import shellplot as plt

# x = np.arange(-4, 4, 0.01)
# y = np.cos(x)
# plt.plot(x, y, xlabel="radians", figsize=(30, 15))
# plt.plot(x, y, xlabel="radians", figsize=(60, 20))
#
#
x = [np.random.randn(100) for i in range(3)]
plt.boxplot(x, labels=np.array(["dist_1", "dist_2", "dist_3"]), figsize=(40, 20))

x = np.random.randn(1000)
plt.hist(x, bins=12, figsize=(40, 20), xlabel="normal distribution")

# x = np.logspace(0, 1, 3)
# plt.barh(
#     x,
#     labels=np.array(["bar_1", "bar_b", "bar_3"]),
#     xlabel="my_fun_bars",
#     figsize=(40, 20),
# )
