import numpy as np

import shellplot as plt

x = np.arange(-3, 6, 0.01)
y1 = np.cos(x)
y2 = np.sin(x)
y3 = y1 + y2

y = np.vstack((y1, y2))
x = np.vstack((x, x))

plt.plot(x, y, labels=("cos", "sin"), figsize=(80, 30))  # , ylim=(-1.5, 1.5))

# plt_str = plt.plot(
#     x,
#     y,
#     figsize=(40, 21),
#     xlim=(0, 3),
#     ylim=(-1, 1),
#     xlabel="x",
#     ylabel="cos(x)",
#     return_type="str",
# )
# print(plt_str)
#
#
# x = [np.random.randn(100) for i in range(3)]
# plt.boxplot(x, labels=np.array(["dist_1", "dist_2", "dist_3"]), figsize=(40, 25))
#
# x = np.random.randn(1000)
# plt.hist(x, bins=12, figsize=(40, 20), xlabel="normal distribution")
#
# x = np.logspace(0, 1, 3)
# plt.barh(
#     x,
#     labels=np.array(["bar_1", "bar_b", "bar_3"]),
#     xlabel="my_fun_bars",
#     figsize=(40, 20),
# )
